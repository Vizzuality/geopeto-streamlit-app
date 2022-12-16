import streamlit as st
from streamlit_folium import st_folium

from functions import show_map

MAP_CENTER = [25.0, 55.0]
MAP_ZOOM = 3

st.set_page_config(
    page_title="mapa",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    # &nbsp; 🌍 &nbsp; Map to analyse Soil organic carbon stock from [soils-revealed](https://soilsrevealed.org/)!
    Follow the instructions in the sidebar on the left to create and download a 3D-printable STL file.
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

print("New action")
print(output)