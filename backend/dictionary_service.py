from typing import Optional
import requests


def get_definition(word: str) -> Optional[str]:
    """
    Get definition for a word.

    Args:
        word: The word to look up (can include punctuation)

    Returns:
        Definition string if found, else a default message
    """
    # Clean the word: lowercase and remove punctuation
    clean_word = word.lower().strip('.,!?;:\'"')

    # api-endpoint
    URL = f"https://api.dictionaryapi.dev/api/v2/entries/en/{clean_word}"

    

    # sending get request and saving the response as response object
    r = requests.get(url = URL)
    if r.status_code == 404:

        return "This word does not have a definition"
    # extracting data in json format
    data = r.json()[0]['meanings'][0]['definitions'][0]['definition']

   
    return data

get_definition("complicatlp")