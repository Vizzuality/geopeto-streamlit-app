import ee
import streamlit as st
from streamlit_folium import st_folium
from shapely.geometry import Polygon, box

from streamlit_map.geocoder import Geocoder
from streamlit_map.geodescriber import GeoDescriber
from streamlit_map.visualize import create_map, create_stacked_bar
from streamlit_map.processing import ZonalStatistics
from streamlit_map.data import GEEData

ee.Initialize()

MAP_CENTER = [25.0, 55.0]
MAP_ZOOM = 3

MAX_ALLOWED_AREA_SIZE = 25.0
BTN_LABEL_COMPUTE = "Compute Zonal Statistics"


def _get_bbox(geojson: dict) -> box:
    # Create a Shapely polygon from the coordinates
    poly = Polygon(geojson['geometry']['coordinates'][0])
    # Get the bbox coordinates using the bounds() method
    min_x, min_y, max_x, max_y = poly.bounds
    # Create the box object using the box() function
    shapely_box = box(min_x, min_y, max_x, max_y)

    return shapely_box


datasets = {}
for dataset in ['Global-Land-Cover', 'Koppen-Geiger-Climate']:
    datasets[dataset] = GEEData(dataset)

if __name__ == "__main__":
    st.set_page_config(
        page_title="mapa",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(
        """
        # &nbsp; 🌍 &nbsp; Map to analyse Global Land Cover!
        Follow the instructions in the sidebar on the left to analyse a region.
        """,
        unsafe_allow_html=True,
    )

    st.write("\n")
    m = create_map(center=MAP_CENTER, zoom=MAP_ZOOM)

    output = st_folium(m, key="init", width=1300, height=600)

    geojson = None
    if output["all_drawings"] is not None:
        if len(output["all_drawings"]) != 0:
            if output["last_active_drawing"] is not None:
                # get latest modified drawing
                geojson = output["last_active_drawing"]


    # ensure progress bar resides at top of sidebar and is invisible initially
    progress_bar = st.sidebar.progress(0)
    progress_bar.empty()

    # Getting Started container
    with st.sidebar.container():
        st.markdown(
            f"""
            # Getting Started
            1. Click the black square on the map
            2. Draw a rectangle on the map
            3. Click on <kbd>{BTN_LABEL_COMPUTE}</kbd>
            """,
            unsafe_allow_html=True,
        )

        # Create an empty container for the plotly figure
        text_container = st.empty()

        # Create an empty container for the plotly figure
        fig_container = st.empty()

        # Add the button and its callback
        if st.button(
            BTN_LABEL_COMPUTE,
            key="compute_zs",
            disabled=False if geojson is not None else True,
        ):
            #data = datasets['Koppen-Geiger-Climate']
            top = {}
            for dataset, data in datasets.items():
                zs = ZonalStatistics(data, MAX_ALLOWED_AREA_SIZE)

                # Call the zs.check_area_and_compute function to get the plotly figure
                stats = zs.check_area_and_compute(geojson=geojson)

                # sort the items from top to bottom and take the top 8 elements
                top_8 = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:8]
                top_8 = {k: v for k, v in top_8}

                top[dataset] = top_8

                if dataset == 'Global-Land-Cover':
                    # Update the empty container with the plotly figure
                    colors = {data.class_names()[key]: item for key, item in
                              data.class_colors().items()}

                    fig = create_stacked_bar(values=stats, colors=colors)
                    fig_container.plotly_chart(fig, use_container_width=True)

            # Update the empty container with the description of the region
            bbox = _get_bbox(geojson=geojson)

            # create Geocoder object
            geolocator = Geocoder(user_agent="my-app")

            # reverse geocode center point of box to get region and country
            center_point = bbox.centroid
            region, country = geolocator.reverse_geocode(center_point)

            print("Region: ", region)
            print("Country: ", country)

            # geodescribe the region with OpenAI API
            geo_describer = GeoDescriber(model_name="text-davinci-003")
            description = geo_describer.generate_description(
                land_cover_per=top['Global-Land-Cover'],
                climate_per=top['Koppen-Geiger-Climate'],
                region_name=region,
                country=country
            )

            text_container.markdown(
                f"""
                **Description of the region:**
                
                {description}
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            4. Wait for the computation to finish
            """,
            unsafe_allow_html=True,
        )



