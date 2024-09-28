```markdown
# GeoCLIP GPS Prediction from Images

This project uses the **GeoCLIP** model to predict GPS coordinates from images. It supports image input via file paths or URLs, generates GPS predictions, displays Google Maps links, and creates interactive maps or world maps. The results can be saved to a CSV file for further use.

based on https://github.com/TIBHannover/GeoEstimation

## Features

- **Image Input:** Accepts images through file paths or URLs.
- **GeoCLIP Model:** Predicts the GPS coordinates of the image.
- **Google Maps Links:** Generates Google Maps links for predicted locations.
- **Interactive Map:** Creates an interactive map using Folium.
- **World Map Plotting:** Plots predictions on a world map using Cartopy.
- **Save Results:** Allows saving the predictions in a CSV file.

## Requirements

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

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/geo-clip-prediction.git
   cd geo-clip-prediction
   ```

2. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up GeoCLIP model weights**:
   Make sure you have the GeoCLIP model weights in the correct directory. If they are not available, download and place them in the appropriate folder.

## Usage

To use the script, simply run the following command:

```bash
python img2loca.py
```

### Features of the Script:

- **Load Model Weights**: The model weights are loaded safely before predictions are made.
- **Image Input**: The user can provide an image via a file path or URL.
- **Predictions**: Predict GPS locations and probabilities for the provided image.
- **Display Results**: The results are displayed along with Google Maps links.
- **Interactive Map**: Option to create an interactive map with Folium.
- **World Map Plot**: Option to plot predictions on a world map using Cartopy.
- **CSV Saving**: Option to save predictions in a CSV file.

### Example Input

The script will prompt you to either provide:

- **Image Path**: Supply the path to an image file on your local machine.
- **Image URL**: Supply the URL to an online image.

Example of running the script:

```bash
python img2loca.py
```

You will be asked to provide an image input type, and then the script will perform predictions and display results.

## Contributing

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.



