import os
import openai
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

openai.api_key = os.getenv("OPENAI_API_KEY")


class GeoDescriber:
    def __init__(self, model_name):
        self.model_name = model_name
        self.prompt = None

    def generate_description(self, land_cover_per, climate_per, region_name, country):
        input_text = f"I am analyzing a region whose centroid has the following address: {region_name}, {country}." \
            f"The Köppen climate classification distribution in that region consists of:"
        for climate, fraction in climate_per.items():
            input_text += f"\n- {fraction:.1f}% {climate}"

        input_text += f"\n\nThe land cover distribution consists of:"

        for land_cover, fraction in land_cover_per.items():
            input_text += f"\n- {fraction:.1f}% {land_cover}"

        #self.prompt = f"{input_text}\n\nDescribe this region without mentioning the percentage of each " \
        #              f"climate classification and land cover type " \
        #              f"and by adding additional socioeconomic information of the region that you may know " \
        #              f"in a paragraph:"

        #self.prompt = f"{input_text}\n\nDescribe the climate, landscape, and geography of this region:"
        self.prompt = f"{input_text}\n\nDescribe the climate, landscape, and socioeconomics of the region:"

        response = openai.Completion.create(
            #engine="davinci",
            model=self.model_name,
            prompt=self.prompt,
            max_tokens=1024, # set a high value for max_tokens to generate longer text
            temperature=1,
            n=1,
            stop=None,  # add a stop sequence to indicate the end of the paragraph
        )
        return response.choices[0].text.strip()


if __name__ == "__main__":
    model_name = "text-davinci-003"
    land_cover_fractions = {
        "Forest": 0.4,
        "Grassland": 0.3,
        "Cropland": 0.2,
        "Wetland": 0.1,
    }

    geo_describer = GeoDescriber(model_name)
    description = geo_describer.generate_description(
        land_cover_fractions,
        region_name="Gipuzkoa",
        ecoregion="Temperate Broadleaf & Mixed Forests",
        country="Spain"
    )
    print(description)
