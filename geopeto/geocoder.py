import re

from geopy.geocoders import Nominatim
from shapely.geometry import box


class Geocoder(Nominatim):
    def __init__(self, user_agent):
        super().__init__(user_agent=user_agent)

    def reverse_geocode(self, center_point):
        location = self.reverse("{}, {}".format(center_point.y, center_point.x), language='en', zoom=8, namedetails=True)
        location = str(location)

        # Remove all occurrences of numbers from the string
        pattern = r'\d+'  # Regular expression pattern matching one or more digits
        location = re.sub(pattern, '', location)

        # Extract region and country from location object
        # Split the resulting string into elements using ', ' as a separator,
        # and filter out any empty strings that may remain
        elements = [e for e in location.split(', ') if e]

        region = ', '.join(elements[:-1])  # Join all elements except the last one with a comma separator
        country = elements[-1]  # Take the last element

        return region, country


if __name__ == '__main__':
    # Define bbox
    bbox = (-2.1860969951349887, 43.04779100897747, -2.16548765387617, 43.058403937201916)

    # Create Shapely box object from bbox
    box_geom = box(*bbox)

    # Create Geocoder object
    geolocator = Geocoder(user_agent="my-app")

    # Reverse geocode center point of box to get region and country
    center_point = box_geom.centroid
    region, country = geolocator.reverse_geocode(center_point)

    print(f"Region: {region}")
    print(f"Location: {country}")
