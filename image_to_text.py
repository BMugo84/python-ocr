def image_processing(image_path: str):
    """Process an anime image to extract specific regions of interest (ROIs).

    Args:
        image_path (str): The file path of the anime image to be processed.

    Returns:
        Tuple[PIL.Image.Image, PIL.Image.Image, PIL.Image.Image, PIL.Image.Image]:
            A tuple of PIL.Image objects representing the following cropped regions:
            - Cropped image representing the year and episodes section.
            - Cropped image representing the title section.
            - Cropped image representing the rating section.
            - Cropped image representing the genre section.

        If any errors occur during image processing, the function returns a tuple of None values.
    """
    try:
        # load the image using PIL
        image = PIL.Image.open(image_path)
        width, height = image.size

        # crop the image to the defined region 
        cropped_image = image.crop(roi)

        width_c, height_c = cropped_image.size


        # Crop the image to the defined region 
        sector_height = height_c // 6
        roi_1 = (0, 0, width_c, sector_height)
        roi_2_3 = (0, sector_height, width_c, 4 * sector_height)
        roi_5 = (0, 4 * sector_height, width_c, 5 * sector_height)
        roi_6 = (0, 5* sector_height, width_c, height_c)

        # Use the already cropped regions for OCR
        year_episodes_image = cropped_image.crop(roi_1)
        title_image = cropped_image.crop(roi_2_3)
        rating_image = cropped_image.crop(roi_5)
        genre_image = cropped_image.crop(roi_6)

        cropped_sections = (year_episodes_image, title_image, rating_image, genre_image)

        # return the cropped images to be used by another function
        return cropped_sections
    
    except Exception as e:
        print(f"Error occurred while processing image: {e}")
        return None
    
def text_extraction(cropped_sections: tuple):
    year_episodes_image, title_image, rating_image, genre_image = cropped_sections

    # convert cropped images to text 
    year_episodes_text = pytesseract.image_to_string(year_episodes_image, config=myconfig)
    title_text = pytesseract.image_to_string(title_image, config=myconfig)
    rating_text = pytesseract.image_to_string(rating_image, config=myconfig)
    genre_text = pytesseract.image_to_string(genre_image, config=myconfig)

    extracted_text = (year_episodes_text, title_text, rating_text, genre_text)
    
    return extracted_text

def cleaning_text(extracted_text: tuple):
    """Clean extracted text data from anime images.

    Args:
        extracted_text (tuple): A tuple containing extracted text from different sections of an anime image.
            The tuple should have the following elements:
            - year_episodes_text (str): Text representing the year and episodes section.
            - title_text (str): Text representing the title section.
            - rating_text (str): Text representing the rating section.
            - genre_text (str): Text representing the genre section.

    Returns:
        tuple: A cleaned tuple containing the following cleaned data:
        - Cleaned year text (str)
        - Cleaned episodes text (int or str)
        - Cleaned title text (str)
        - Cleaned rating text (int or str)
        - Cleaned genre text (str)
    """
    year_episodes_text, title_text, rating_text, genre_text = extracted_text

    # cleaning year_episodes
    if year_episodes_text:
        # extract year and episodes from the year_episodes_text

        # Define a list of possible signs
        split_signs = ["¢", "°", "+", "°", "¢", "©", "¢", "¢", "«", "*"]

        year_episodes_split = None  # Initialize the split variable

        # Try to split using each sign
        for sign in split_signs:
            if sign in year_episodes_text:
                year_episodes_split = year_episodes_text.split(sign)
                break  # Stop searching if a valid split is found

        if year_episodes_split is not None:
            year_text = year_episodes_split[0]
            episodes_text = year_episodes_split[1]
        else:
            # If no valid split is found, use the original text
            year_text = year_episodes_text
            episodes_text = "not defined"   
    else:
        year_text = "not defined"
        episodes_text = "not defined"           

    # clean up year
    year_text = year_text.replace('\n', ' ')

    # convert episodes to integers
    if episodes_text != "not defined" and episodes_text:
        # Use regular expression to extract integers
        episodes_integers = re.findall(r'\d+', episodes_text)
        if episodes_integers:
            episodes_integer = int(''.join(episodes_integers))
        else:
            episodes_integer = "not defined"
    else:
        episodes_integer = "not defined"  


    # cleaning title
    if title_text:
        # clean up title
        title_text = title_text.replace('\n', ' ')
    else:
        title_text = "not defined"


    # cleaning up ratings
    if rating_text:
        # Convert the list of integers to a single string or integer value
        rating_integers = re.findall(r'\d+', rating_text)
        if len(rating_integers) > 1:
            # Use regular expression to extract integers
            rating_integer = int(''.join(rating_integers))
        else:
            rating_integer =  "not defined"
    else:
        rating_integer = "not defined"


    # cleaning up genres
    if genre_text:
        # clean up genres
        genre_text = genre_text.replace('\n', '')
    else:
        genre_text = "not defined"

    
    # print(year_text)
    # print(episodes_integer)
    # print(title_text)
    # print(rating_integer)
    # print(genre_text)

    cleaned_text = (year_text, episodes_integer, title_text, rating_integer, genre_text)

    return cleaned_text

def add_data_to_df(cleaned_text: tuple):
    year_text, episodes_integer, title_text, rating_integer, genre_text = cleaned_text

    row_data = {
        "Year": year_text,
        "Episodes": episodes_integer,
        "Title": title_text,
        "Rating": rating_integer,
        "Genres": genre_text
    }

    df.loc[len(df)] = row_data  


os.chdir("C:/Users/BM/python_ocr/anime_alpha_photos/photos")


image_paths = []
for file in os.listdir():
    image_paths.append(file)


# Clear the DataFrame
df.drop(index=df.index, inplace=True)

for image_path in image_paths:
    cropped_sections = image_processing(image_path)
    extracted_text = text_extraction(cropped_sections) # type: ignore
    cleaned_text = cleaning_text(extracted_text)

    # add data to df
    add_data_to_df(cleaned_text)

    print(f'{image_path} done!')

# print the dataframe
pd.set_option('display.width', 1000)
print(df)

pd.set_option('display.max_rows', None)
print(df)