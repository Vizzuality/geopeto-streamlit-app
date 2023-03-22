import logging

import ee
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from .utils import get_region
from .verification import selected_bbox_in_boundary, selected_bbox_too_large


def create_stacked_bar(values, colors):
    # create a list of categories (keys in values dictionary)
    labels = list(values.keys())

    # create a list of values for each category
    values = [values[cat] for cat in labels]

    # create a list of colors for each category
    colors = [colors[cat] for cat in labels]

    dic = dict(zip(labels, values))

    width = 0.35  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots(figsize=(10, 1))
    left_value = 0
    for n, label in enumerate(dic.keys()):
        ax.barh([' '], [dic[label]], width, left=left_value, label=label, color=colors[n], ec=colors[n])
        ax.margins(x=0)

        left_value += dic[label]

    return fig


def create_stacked_bar_plotly(values, colors):
    # create a list of categories (keys in values dictionary)
    labels = list(values.keys())

    # create a list of values for each category
    values_list = [values[cat] for cat in labels]

    # create a list of colors for each category
    colors_list = [colors[cat] for cat in labels]

    # Define the data for the stacked bar chart
    data = [
        go.Bar(
            x=values_list,
            y=labels,
            orientation='h',
            name=labels[i],
            marker=dict(color=colors_list[i])
        )
        for i in range(len(labels))
    ]

    # Define the layout for the stacked bar chart
    layout = go.Layout(
        barmode='stack',
        height=150,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=True, zeroline=False),
    )

    # Create the stacked bar chart figure
    fig = go.Figure(data=data, layout=layout)

    return fig


class ZonalStatistics:
    def __init__(self, gee_data, max_allowed_area_size: float = 25.):
        self.gee_data = gee_data
        self.max_allowed_area_size = max_allowed_area_size

    def check_area_and_compute(self, geojson: dict, progress_bar: st.progress) -> None:
        geometry = geojson['geometry']
        if selected_bbox_too_large(geometry, threshold=self.max_allowed_area_size):
            st.sidebar.warning(
                "Selected region is too large, fetching data for this area would consume too many resources. "
                "Please select a smaller region."
            )
        elif not selected_bbox_in_boundary(geometry):
            st.sidebar.warning(
                "Selected rectangle is not within the allowed region of the world map. "
                "Do not scroll too far to the left or right. "
                "Ensure to use the initial center view of the world for drawing your rectangle."
            )
        else:
            stats = self.compute(geometry, progress_bar)

            fig = create_stacked_bar(values=stats['b1'], colors=self.gee_data.class_colors())

            # it is important to spawn this success message in the sidebar, because state will get lost otherwise
            st.sidebar.success("Successfully computed Zonal Statistics!")

            return fig

    def compute(self, geometry: dict, progress_bar: st.progress) -> None:
        region = get_region(geometry)  # Create an EE feature
        img = self.gee_data.ee_image()
        try:
            stats = img.reduceRegion(**{'reducer': ee.Reducer.frequencyHistogram(),
                                        'geometry': region,
                                        'bestEffort': True,
                                        }).getInfo()
            logging.info(f'[ZonalStatistics]: stats: {stats}')
        except:
            logging.error('[ZonalStatistics]: EE failed.')
            stats = {}

        return stats

