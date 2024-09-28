import torch
import torch.nn as nn
from geoclip import GeoCLIP
from PIL import Image
import os
import requests
import folium
import csv
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Initialize the GeoCLIP model
model = GeoCLIP()

# Function to validate and preprocess an image
def validate_and_preprocess_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Le fichier {image_path} n'existe pas.")
    try:
        img = Image.open(image_path)
        img.verify()
        print("Validation de l'image réussie.")
        return img
    except (IOError, SyntaxError) as e:
        raise ValueError(f"Fichier image invalide : {image_path}") from e

# Function to download an image from a URL
def download_image(image_url, save_path='downloaded_image.jpg'):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Image téléchargée avec succès : {save_path}")
        return save_path
    else:
        raise ValueError(f"Échec du téléchargement de l'image depuis {image_url}")

# Function to generate a Google Maps link
def generate_google_maps_link(lat, lon):
    return f"https://www.google.com/maps?q={lat},{lon}"

# Function to create an interactive map with Folium
def create_interactive_map(predictions, probabilities, output_file='predicted_locations_map.html'):
    avg_lat = sum([lat for lat, _ in predictions]) / len(predictions)
    avg_lon = sum([lon for _, lon in predictions]) / len(predictions)
    map_ = folium.Map(location=[avg_lat, avg_lon], zoom_start=2)

    for i, (lat, lon) in enumerate(predictions):
        folium.Marker(
            location=[lat, lon],
            popup=f'Prédiction {i+1}: ({lat:.6f}, {lon:.6f})',
            tooltip=f'Probabilité: {probabilities[i]:.6f}'
        ).add_to(map_)

    map_.save(output_file)
    print(f"Carte interactive créée : {output_file}")

# Function to plot GPS predictions on a world map using Cartopy
def plot_predictions_on_map(predictions):
    fig = plt.figure(figsize=(10, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()

    for lat, lon in predictions:
        ax.plot(lon, lat, marker='o', color='red', markersize=8, transform=ccrs.Geodetic())

    plt.title('Localisations GPS Prédites')
    plt.show()

# Function to save the prediction results to a CSV file
def save_results_to_file(predictions, probabilities, file_name="predictions.csv"):
    if not file_name.strip():
        print("Erreur : le nom du fichier ne peut pas être vide.")
        return

    directory = os.path.dirname(file_name)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Prédiction", "Latitude", "Longitude", "Probabilité", "Lien Google Maps"])
            for i, ((lat, lon), prob) in enumerate(zip(predictions, probabilities)):
                google_maps_link = generate_google_maps_link(lat, lon)
                writer.writerow([f"Prédiction {i+1}", lat, lon, prob, google_maps_link])
        print(f"Résultats enregistrés dans {file_name}")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'enregistrement du fichier : {e}")

# Function to ask the user how many predictions they want to see
def get_user_top_k():
    while True:
        try:
            top_k = int(input("Combien de prédictions voulez-vous voir ? "))
            if top_k > 0:
                return top_k
            else:
                print("Veuillez entrer un nombre positif.")
        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre entier.")

# Function to get the image input (URL or path)
def get_image_input():
    while True:
        choice = input("Souhaitez-vous fournir un chemin d'image ou une URL ? (Entrez 'path' ou 'url'): ").strip().lower()
        if choice == 'url':
            image_url = input("Veuillez entrer l'URL de l'image : ").strip()
            try:
                return download_image(image_url)
            except ValueError as e:
                print(e)
        elif choice == 'path':
            image_path = input("Veuillez entrer le chemin du fichier image : ").strip()
            try:
                validate_and_preprocess_image(image_path)
                return image_path
            except (FileNotFoundError, ValueError) as e:
                print(e)
        else:
            print("Choix invalide. Veuillez entrer 'path' ou 'url'.")

# Function to load the model weights safely using weights_only=True
def load_model_weights_safely():
    model.image_encoder.mlp.load_state_dict(torch.load(f"{model.weights_folder}/image_encoder_mlp_weights.pth", weights_only=True))
    model.location_encoder.load_state_dict(torch.load(f"{model.weights_folder}/location_encoder_weights.pth", weights_only=True))
    model.logit_scale = nn.Parameter(torch.load(f"{model.weights_folder}/logit_scale_weights.pth", weights_only=True))
    print("Model weights loaded successfully.")

# Main function to handle predictions and additional functionalities
def main():
    # Load model weights safely
    load_model_weights_safely()

    # Get image input (URL or path)
    image_path = get_image_input()

    # Get the number of top predictions
    top_k = get_user_top_k()

    # Perform the prediction
    top_pred_gps, top_pred_prob = model.predict(image_path, top_k=top_k)

    # Display the results
    print("\nPrédictions GPS")
    print("=====================")
    for i in range(top_k):
        lat, lon = top_pred_gps[i]
        google_maps_link = generate_google_maps_link(lat, lon)
        print(f"Prédiction {i+1}: ({lat:.6f}, {lon:.6f})")
        print(f"Probabilité: {top_pred_prob[i]:.6f}")
        print(f"Lien Google Maps: {google_maps_link}")
        print("")

    # Ask if the user wants to save the results
    save_option = input("Souhaitez-vous enregistrer les résultats dans un fichier CSV ? (oui/non) : ").strip().lower()
    if save_option == 'oui':
        save_file = input("Entrez le nom du fichier (ex : 'predictions.csv') : ").strip()
        save_results_to_file(top_pred_gps, top_pred_prob, file_name=save_file)

    # Ask if the user wants to create an interactive map
    map_option = input("Souhaitez-vous créer une carte interactive des prédictions ? (oui/non) : ").strip().lower()
    if map_option == 'oui':
        map_file = input("Entrez le nom du fichier de la carte (ex : 'map.html') : ").strip()
        create_interactive_map(top_pred_gps, top_pred_prob, output_file=map_file)

    # Ask if the user wants to plot the predictions on a world map
    plot_option = input("Souhaitez-vous tracer les prédictions sur une carte mondiale ? (oui/non) : ").strip().lower()
    if plot_option == 'oui':
        plot_predictions_on_map(top_pred_gps)

# Run the main function
if __name__ == "__main__":
    main()
