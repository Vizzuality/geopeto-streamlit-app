# Geopeto Streamlit App

This repository contains a Streamlit app where the user can select a region and get land cover and Köppen climate classification data from Google Earth Engine. The app also uses the Nominatim geocoder for OpenStreetMap data and the OpenAI API for geodescribing the region based on the data provided.

![](images/demo.gif)

## Installation

To use the app, follow these steps:

1. Clone the repository: `git clone git@github.com:Vizzuality/geopeto-streamlit-app.git`
2. Change into the repository directory: `cd geopeto-streamlit-app`
3. Create a virtual environment: `python -m venv env`
4. Activate the virtual environment: `source env/bin/activate`
5. Install the required packages: `pip install -r requirements.txt`
6. Create a `.env` file with your Google Earth Engine private key and OpenAI API key:

    ```
    EE_PRIVATE_KEY=your_google_earth_engine_private_key
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

To run the app, use the following command:

```
streamlit run app.py
```

This will launch the app in your default web browser.

1. Click the black square on the map
2. Draw a rectangle on the map
3. Click on `Compute Zonal Statistics`
4. Wait for the computation to finish

## Contributing

If you find a bug or want to suggest a feature, please create a new issue on the GitHub repository. Pull requests are also welcome.


