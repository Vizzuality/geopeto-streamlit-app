import ee
import streamlit as st
from streamlit_folium import st_folium

from streamlit_map.map import show_map
from streamlit_map.processing import ZonalStatistics
from streamlit_map.data import GEEData

ee.Initialize()

MAP_CENTER = [25.0, 55.0]
MAP_ZOOM = 3

MAX_ALLOWED_AREA_SIZE = 25.0
BTN_LABEL_COMPUTE = "Compute Zonal Statistics"

gee_data = GEEData('Global-Land-Cover')
zs = ZonalStatistics(gee_data, MAX_ALLOWED_AREA_SIZE)

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
    m = show_map(center=MAP_CENTER, zoom=MAP_ZOOM)

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

        # Plot!
        # Create an empty container for the plotly figure
        fig_container = st.empty()

        # Add the button and its callback
        if st.button(
            BTN_LABEL_COMPUTE,
            key="compute_zs",
            disabled=False if geojson is not None else True,
        ):
            # Call the zs.check_area_and_compute function to get the plotly figure
            fig = zs.check_area_and_compute(geojson=geojson, progress_bar=progress_bar)

            # Update the empty container with the plotly figure
            #fig_container.plotly_chart(fig, use_container_width=True)
            fig_container.pyplot(fig, bbox_inches='tight', pad_inches=0)

        st.markdown(
            f"""
            4. Wait for the computation to finish
            """,
            unsafe_allow_html=True,
        )


    print("State")
    print("folium_output: ", output)
    print("Session: ", st.session_state)
    if geojson is not None:
        print("geojson: ", geojson.get('geometry'))


