import re
from typing import List, Dict
from dictionary_service import get_definition
from wordfreq import zipf_frequency

def tokenize(text: str) -> List[str]:
    """
    Split text into words and punctuation.

    Example:
        "Hello, world!" → ["Hello", ",", "world", "!"]

    Why? We want to preserve punctuation in output but analyze it separately.
    """
    # Regex pattern:
    # \w+ matches one or more word characters (letters, numbers, underscore)
    # | means "or"
    # [.,!?;] matches individual punctuation marks
    tokens = re.findall(r"[\w']+|[.,!?;]", text)
    return tokens

def is_hard_word(word: str) -> bool:

    """
    Determine if a word is "hard" based on length.

    Simple rule: words longer than 7 characters are considered hard.

    Note: This is a simple heuristic. More advanced versions could:
    - Check word frequency (rare words are harder)
    - Use reading level algorithms (Flesch-Kincaid, etc.)
    - Call an external API for difficulty scoring
    """
    # 0 8
    freq = zipf_frequency(word, 'en', wordlist='best', minimum=0) 
    print(freq)
    if  freq < 5:
        return True
    else :
        return False
    

def analyze_text(text: str) -> List[Dict]:
    """
    Analyze text and return metadata for each word.

    Args:
        text: Raw text string to analyze

    Returns:
        List of dictionaries with structure:
        {
            "word": "loquacious",
            "is_hard": True,
            "definition": "Tending to talk a great deal"
        }
    """
    # Step 1: Tokenize
    tokens = tokenize(text)

    # Step 2: Analyze each token
    results = []
    for token in tokens:
        if token.isalpha() == True:
            is_hard = is_hard_word(token)
        

        # Get definition only for hard words
        definition = None
        if is_hard:
            definition = get_definition(token)

        # Build result object
        results.append({
            "word": token,
            "is_hard": is_hard,
            "definition": definition
        })

    return results
