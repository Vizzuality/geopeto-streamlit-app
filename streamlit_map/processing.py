import logging

import ee
import streamlit as st

from .utils import get_region
from .verification import selected_bbox_in_boundary, selected_bbox_too_large


def serialize_output(data):
    # Sort stats by key value
    data = data['b1']
    data = {int(k): data[k] for k in data}
    data = {str(k): data[k] for k in sorted(data)}

    return data


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
            # it is important to spawn this success message in the sidebar, because state will get lost otherwise
            st.sidebar.success("Successfully computed Zonal Statistics!")

            stats = self.compute(geometry, progress_bar)

            # Sort stats by key value
            stats = serialize_output(stats)

            # convert each item to percentages
            total_area = sum(stats.values())
            stats = {key: (item / total_area) * 100 for key, item in stats.items()}

            # add class names
            stats = {self.gee_data.class_names()[key]: item for key, item in stats.items()}

            print('Stats: ', stats)

            return stats

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

