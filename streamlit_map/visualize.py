from typing import List

import ee
import folium
import pandas as pd
from folium.plugins import Draw
from branca.element import MacroElement
from plotly import express as px
import ipyleaflet as ipyl

from .data import GEEData


class foliumMapGEE(folium.Map):
    """
    A custom Map class that can display Google Earth Engine tiles.

    Inherits from folium.Map class.
    """

    def __init__(self,  center: List[float] = [25.0, 55.0], zoom: int = 3, **kwargs):
        """
        Constructor for MapGEE class.

        Parameters:
        center: list, default [25.0, 55.0]
            The current center of the map.
        zoom: int, default 3
            The current zoom value of the map.
        **kwargs: Additional arguments that are passed to the parent constructor.
        """
        self.center = center
        self.zoom = zoom
        self.geometry = None
        super().__init__(#tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
                         location=self.center, zoom_start=self.zoom, control_scale=True, 
                         attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>', **kwargs)
        
        self.add_draw_control()
        
    def add_draw_control(self):
        draw = Draw(
            export=False,
            position="topleft",
            draw_options={
                "polyline": False,
                "poly": False,
                "circle": False,
                "polygon": False,
                "marker": False,
                "circlemarker": False,
                "rectangle": True
                }
            )
        
        draw.add_to(self)
        
        # Add a listener that captures the drawn items by the user and stores the geometry of the polygon in self.geometry.
        js = '''
        function getGeometry(e) {
            var geometry = e.layer.toGeoJSON().geometry;
            var command = "window.parent.mapvw.geometry = " + JSON.stringify(geometry) + ";";
            console.log(command);
            eval(command);
        };

        window.parent.mapvw.map.on('draw:created', getGeometry);
        '''

        self.add_child(MacroElement().add_child(folium.Html(js)))
        
    def add_gee_layer(self, image: ee.Image, sld_interval: str, name: str):
        """
        Add GEE layer to map.

        Parameters:
        image (ee.Image): The Earth Engine image to display.
        sld_interval (str): SLD style of discrete intervals to apply to the image.
        name (str): lLayer name.
        """
        ee_tiles = '{tile_fetcher.url_format}'
        
        image = image.sldStyle(sld_interval)
        mapid = image.getMapId()
        tiles_url = ee_tiles.format(**mapid)
        
        tile_layer = folium.TileLayer(
            tiles=tiles_url, 
            name=name,
            attr=name,
            overlay=True,
            control=True,
            opacity=1
            )
        
        tile_layer.add_to(self)
        
    def add_layer_control(self):
        control = folium.LayerControl(position='topright')
        
        control.add_to(self)
        

class ipyleafletMapGEE(ipyl.Map):
    """
    A custom Map class that can display Google Earth Engine tiles.

    Inherits from ipyl.Map class.
    """

    def __init__(self,  center: List[float] = [25.0, 55.0], zoom: int = 3, **kwargs):
        """
        Constructor for MapGEE class.

        Parameters:
        center: list, default [25.0, 55.0]
            The current center of the map.
        zoom: int, default 3
            The current zoom value of the map.
        **kwargs: Additional arguments that are passed to the parent constructor.
        """
        self.center = center
        self.zoom = zoom
        self.geometry = None
        super().__init__(basemap=ipyl.basemap_to_tiles(ipyl.basemaps.OpenStreetMap.Mapnik),
                         center=self.center, zoom=self.zoom, **kwargs)
        
        self.add_draw_control()
        
    def add_draw_control(self):
        control = ipyl.LayersControl(position='topright')
        self.add_control(control)
        
        # Add DrawControl
        print('Draw a rectangle on map to select and area.')

        draw_control = ipyl.DrawControl(position='topleft')
        draw_control.display_iframe = True

        draw_control.rectangle = {
            "shapeOptions": {
                "color": "#2BA4A0",
                "fillOpacity": 0,
                "opacity": 1
            }
        }

        feature_collection = {
            'type': 'FeatureCollection',
            'features': []
        }

        def handle_draw(self, action, geo_json):
            """Do something with the GeoJSON when it's drawn on the map"""    
            # feature_collection['features'].append(geo_json)
            feature_collection['features'] = geo_json

        draw_control.on_draw(handle_draw)
        self.add_control(draw_control)

        self.geometry = feature_collection
    
    def add_gee_layer(self, image: ee.Image, sld_interval: str, name: str):
        """
        Add GEE layer to map.

        Parameters:
        image (ee.Image): The Earth Engine image to display.
        sld_interval (str): SLD style of discrete intervals to apply to the image.
        name (str): lLayer name.
        """
        ee_tiles = '{tile_fetcher.url_format}'
        
        image = image.sldStyle(sld_interval)
        mapid = image.getMapId()
        tiles_url = ee_tiles.format(**mapid)
        
        tile_layer = ipyl.TileLayer(url=tiles_url, name=name)
        
        self.add_layer(tile_layer)
    

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
