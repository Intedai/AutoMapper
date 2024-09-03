from PIL import Image, ImageDraw, ImageFont
import re
from globals import ASSETS_PATH, FONT_PATH, FONT
from os import path

def parse_colored_text(text: str) -> list:
    """
    Parse title text into a list of words and their color
    :param text: text to parse
    :returns: the list of the parsed text
    """

    # Regular expression to find words with color codes EXAMPLE: &(#ff0000)Word
    pattern = re.compile(r'&\((#[0-9a-fA-F]{6})\)([^\s&]+)|([^\s&]+)')
    matches = pattern.findall(text)

    parsed_text = []

    for match in matches:
        # If no color specified add None as the color
        color = match[0] if match[0] else None
        word = match[1] if match[1] else match[2]
        parsed_text.append((word, color))
    
    return parsed_text

def generate_outlined_text(x, y, text: str, size: tuple, text_size: int, fill_color: tuple, stroke_color: tuple, stroke_width: int) -> Image.Image:
    """
    Generate image of the outlined text
    :param x: the x-coordinate of the text
    :param y: the y-coordinate of the text
    :param text: the outlined text
    :param size: image size
    :param text_size: text size
    :param fill_color: color of the text
    :param stroke_color: color of the outline
    :param stroke_width: size of the outline
    :returns: image with the outlined text
    """
    im = Image.new('RGBA', size)
    font = ImageFont.truetype(path.join(ASSETS_PATH,FONT_PATH,FONT), text_size)
    drawer = ImageDraw.Draw(im)

    # Split the text into lines where <BR> appears
    lines = text.split('<BR>')  

    W, H = im.size

    # Calculate the total height of the text block
    line_height = text_size
    text_block_height = line_height * len(lines)

    if x == -1 and y == -1:
        # Center the text block vertically
        text_y = (H - text_block_height) // 2
    else:
        text_y = y

    for line in lines:
        # Parse the text to get the colors
        words_with_colors = parse_colored_text(line)
        
        text_x = x if x != -1 else 0
        total_line_width = sum([drawer.textbbox((0, 0), word, font=font)[2] - drawer.textbbox((0, 0), word, font=font)[0] + drawer.textbbox((0, 0), ' ', font=font)[2] - drawer.textbbox((0, 0), ' ', font=font)[0] for word, _ in words_with_colors])
        
        if x == -1:
            text_x = (W - total_line_width) // 2

        for word, word_color in words_with_colors:
            # Calculate the width of the current word
            text_bbox = drawer.textbbox((0, 0), word, font=font)
            text_width = text_bbox[2] - text_bbox[0]

            # Draw the word with the specified color or default fill color if its None
            color = word_color if word_color else fill_color
            drawer.text((text_x, text_y), word, font=font, fill=color, stroke_width=stroke_width, stroke_fill=stroke_color)

            # Move the x position for the next word
            space_width = drawer.textbbox((0, 0), ' ', font=font)[2] - drawer.textbbox((0, 0), ' ', font=font)[0]
            
            # Add space width between words
            text_x += text_width + space_width

        # Move the y position for the next line
        text_y += line_height

    return im
