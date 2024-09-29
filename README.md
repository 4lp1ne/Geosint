---

### GeoCLIP GPS Prediction from Images

This project uses the GeoCLIP model to predict GPS coordinates from images. It supports image input via file paths or URLs, generates GPS predictions, displays Google Maps links, and creates interactive maps or world maps. The results can be saved to a CSV file for further use.

Based on [GeoEstimation](https://github.com/TIBHannover/GeoEstimation).

---

### Features

- **Image Input**: Accepts images through file paths or URLs.
- **GeoCLIP Model**: Predicts the GPS coordinates of the image.
- **Google Maps Links**: Generates Google Maps links for predicted locations.
- **Interactive Map**: Creates an interactive map using Folium.
- **World Map Plotting**: Plots predictions on a world map using Cartopy.
- **Save Results**: Allows saving the predictions in a CSV file.

---

### Requirements

To run the project, you'll need the following Python packages:

- `torch`
- `geoclip`
- `Pillow`
- `requests`
- `folium`
- `matplotlib`
- `cartopy`

You can install these dependencies by running the following command:

```bash
pip install torch geoclip Pillow requests folium matplotlib cartopy
```

---

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/4lp1ne/geosint
    cd geosint
    ```

2. **Create and activate a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up GeoCLIP model weights**:
   - The script will automatically download the GeoCLIP model weights if they are not already present in the `weights/` directory.
   - Alternatively, ensure you have the GeoCLIP model weights in the correct directory (`weights/geoclip_weights.pth`).

---

### GeoCLIP Model Weights Handling

The model weights will be downloaded automatically if they are not found in the `weights/` folder. You can also manually download the weights and place them in this directory if you prefer. The script will then load these weights before making predictions.

Here’s how the process works:

1. **Check and download weights if necessary**:  
   The script first checks whether the weights are present in the directory. If they are missing, it downloads them from a specified URL:

    ```python
    def download_weights():
        if not os.path.exists(WEIGHTS_FILE):
            print("GeoCLIP model weights not found, downloading...")
            response = requests.get(WEIGHTS_URL)
            with open(WEIGHTS_FILE, "wb") as f:
                f.write(response.content)
            print("GeoCLIP model weights downloaded successfully!")
        else:
            print("GeoCLIP model weights found!")
    ```

2. **Load the model with weights**:  
   Once the weights are downloaded or available, the script loads them into the GeoCLIP model:

    ```python
    def load_model():
        download_weights()  # Ensure weights are downloaded before loading the model
        model = GeoCLIP()
        model.load_state_dict(torch.load(WEIGHTS_FILE, map_location=torch.device('cpu')))
        model.eval()  # Set the model to evaluation mode
        print("GeoCLIP model loaded successfully!")
        return model
    ```

---

### Usage

To use the script, simply run the following command:

```bash
python geosint.py
```

#### Features of the Script:
- **Load Model Weights**: The model weights are loaded automatically before predictions are made. If the weights are not found locally, they are downloaded.
- **Image Input**: The user can provide an image via a file path or URL.
- **Predictions**: Predict GPS locations and probabilities for the provided image.
- **Display Results**: The results are displayed along with Google Maps links.
- **Interactive Map**: Option to create an interactive map with Folium.
- **World Map Plot**: Option to plot predictions on a world map using Cartopy.
- **CSV Saving**: Option to save predictions in a CSV file.

---

### Example Input

The script will prompt you to either provide:

- **Image Path**: Supply the path to an image file on your local machine.
- **Image URL**: Supply the URL to an online image.

Example of running the script:

```bash
python geosint.py
```

You will be asked to provide an image input type, and then the script will perform predictions and display results.

---

### Contributing

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

---
