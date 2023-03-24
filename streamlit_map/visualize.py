from typing import List

import ee
import folium
import pandas as pd
from folium.plugins import Draw
from plotly import express as px

from .data import GEEData


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


def create_map(center: List[float], zoom: int) -> folium.Map:
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
    gee_data = GEEData('Global-Land-Cover')

    tile_layer = TileLayerGEE(
        image=gee_data.ee_image(),
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


def create_stacked_bar(values, colors):
    # create a DataFrame with the items of the values dictionary
    df = pd.DataFrame(list(values.items()), columns=["label", "value"])
    df['y_axis'] = ' '

    # create a horizontal bar chart for each category
    fig = px.bar(
        df,
        y="y_axis",
        x='value',
        color="label",
        color_discrete_map=colors,
        hover_data={"y_axis": False, "value": ":,.2f", "label": True}
    )

    fig.update_layout(
        title="Summary Metrics",
        showlegend=False,
        height=200,
        width=800
    )

    # remove x and y axis titles and x-axis tick labels
    fig.update_xaxes(title=None, showticklabels=False)
    fig.update_yaxes(title=None)

    return fig
