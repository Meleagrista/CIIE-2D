from unidecode import unidecode


def replace_accented_characters(text):
    """
    Replace accented characters with their base characters.

    Parameters:
        text (str): The input text with accented characters.

    Returns:
        str: The text with accented characters replaced by their base characters.
    """
    return unidecode(text)
