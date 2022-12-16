import streamlit as st
from streamlit_folium import st_folium

from functions import show_map

MAP_CENTER = [25.0, 55.0]
MAP_ZOOM = 3

BTN_LABEL_COMPUTE = "Compute Zonal Statistics"

st.set_page_config(
    page_title="mapa",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    # &nbsp; 🌍 &nbsp; Map to analyse SOC stock from [soils-revealed](https://soilsrevealed.org/)!
    Follow the instructions in the sidebar on the left to analyse a region.
    """,
    unsafe_allow_html=True,
)
st.write("\n")
m = show_map(center=MAP_CENTER, zoom=MAP_ZOOM)
output = st_folium(m, key="init", width=1300, height=600)

if output:
    if output["last_active_drawing"] is not None:
        # get latest modified drawing
        geometry = output["last_active_drawing"]

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
    st.button(
        BTN_LABEL_COMPUTE,
        key="compute_zs",
        #on_click=_check_area_and_compute_stl,
        #kwargs={"folium_output": output, "geo_hash": geo_hash, "progress_bar": progress_bar},
    )
    st.markdown(
        f"""
        4. Wait for the computation to finish
        """,
        unsafe_allow_html=True,
    )
print("State")
print(st.session_state)

