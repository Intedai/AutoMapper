from PIL import Image
import numpy as np
import os
from typing import Tuple
from globals import ASSETS_PATH, COUNTRIES_PATH, OUTLINE_PATH, WHITE, BLACK, SIZE
from text_generation import generate_outlined_text
from dictionaries import position_dict

def _modify_color(image_path: str, old_color: Tuple[int,int,int], new_color: Tuple[int,int,int]) -> Image.Image:
    """
    Efficient function to replace color inside an image
    :param image_path: path of the image
    :param old_color: color that will be replaced
    :param new_color: color that will replace the old color
    :returns: image with the replaced color
    """

    original_image = Image.open(image_path).convert("RGBA")
    data = np.array(original_image)

    red, green, blue, alpha = data.T
    
    old_color_areas = (red == old_color[0]) & (blue == old_color[1]) & (green == old_color[2])
    data[..., :-1][old_color_areas.T] = new_color
    new_image = Image.fromarray(data)
    
    return new_image

def _make_map_colored(color_country_dict: dict) -> Image.Image:
    """
    Make a map with colored countries according to a color dict
    :param color_country_dict: country dictionary with the colors of each country
    :returns: image of the map with colored countries
    """
    map_image = Image.new("RGBA", (1080, 1920), (0,0,0,0))
    outline_image = Image.open(os.path.join(ASSETS_PATH,COUNTRIES_PATH,OUTLINE_PATH))

    # Get all country images (this includes the outline)
    files = os.listdir(os.path.join(ASSETS_PATH,COUNTRIES_PATH))
    
    # Remove the outline from countries list because it's pasted in the end
    files.remove(OUTLINE_PATH)
    
    # Color each country according to the dict and paste it onto the map
    for file in files:
        country_image = _modify_color(os.path.join(ASSETS_PATH,COUNTRIES_PATH, file), WHITE,color_country_dict[file])
        map_image.paste(country_image, (0,0), country_image)
    
    # Paste the outline on top of the map
    map_image.paste(outline_image, (0,0), outline_image)

    return map_image

def make_text_map_colored(top_text: str, years_dict: dict, color_country_dict: dict) -> Image.Image:
    """
    Make the final map image, with colored countries text in the top
    and years on every country
    :param top_text: Text that will appear in the top of the image
    :param years_dict: dictionary of the years that appear on each country
    :param color_country_dict: country dictionary with the colors of each country
    """

    # Make colored map
    map_image = _make_map_colored(color_country_dict)

    # Generate title
    top_text = generate_outlined_text(-1,150, top_text,SIZE,70,WHITE,BLACK,5)

    # Paste title on top
    map_image.paste(top_text, (0,0), top_text)

    # Write a year on each country
    for country, position in position_dict.items():
        year_text = generate_outlined_text(position[0], position[1], years_dict[country], (1080, 1920), 40 * position[2], WHITE, BLACK, 2)
        map_image.paste(year_text, (0, 0), year_text)

    return map_image
