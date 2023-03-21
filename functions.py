from typing import List

import folium
from folium.plugins import Draw
import ee

from data import GEEData

ee.Initialize()


class TileLayerGEE(folium.TileLayer):
    """
    A custom TileLayer class that can display Google Earth Engine tiles.

    Inherits from folium.TileLayer class.
    """
    ee_tiles = '{tile_fetcher.url_format}'

    def __init__(self, image: ee.Image, sld_interval: str, name: str, **kwargs):
        """
        Constructor for TileLayerGEE class.

        Parameters:
        image (ee.Image): The Earth Engine image to display.
        sld_interval (str): SLD style of discrete intervals to apply to the image.
        name (str): lLayer name.
        **kwargs: Additional arguments that are passed to the parent constructor.
        """
        self.image = image
        self.sld_interval = sld_interval
        self.name = name
        super().__init__(tiles=self.get_tile_url(), **kwargs)

    def get_tile_url(self):
        self.image = self.image.sldStyle(self.sld_interval)
        mapid = self.image.getMapId()
        tiles_url = self.ee_tiles.format(**mapid)

        return tiles_url


def show_map(center: List[float], zoom: int) -> folium.Map:
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        control_scale=True,
        tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',  # noqa: E501
    )
    Draw(
        export=False,
        position="topleft",
        draw_options={
            "polyline": False,
            "poly": False,
            "circle": False,
            "polygon": False,
            "marker": False,
            "circlemarker": False,
            "rectangle": True,
        },
    ).add_to(m)

    # Add a TileLayer with the provided URL
    gee_data = GEEData('Current-SOC-stocks-(0-200-cm)')

    tile_layer = TileLayerGEE(
        image=ee.Image(gee_data.asset_id()),
        sld_interval=gee_data.sld_interval(),
        name=gee_data.dataset,
        attr=gee_data.dataset,
        overlay=True,
        control=False,
        opacity=1
    )

    tile_layer.add_to(m)

    #control = folium.LayerControl(position='topright')
    #control.add_to(m)

    return m



