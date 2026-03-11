import re
from typing import List, Dict, Optional
from dictionary_service import get_definition
from wordfreq import zipf_frequency
import concurrent.futures


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
    """Return True if `word` is considered hard using frequency heuristics.

    The function expects a normalized, lowercase alphabetic word.
    """
    if not word:
        return False
    try:
        freq = zipf_frequency(word, 'en', wordlist='best', minimum=0)
    except Exception:
        return False
    return freq < 5
    

def _is_word_token(token: str) -> bool:
    return re.fullmatch(r"[A-Za-z']+", token) is not None


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

    # Build normalized mapping for tokens (preserve original order)
    entries = []
    for token in tokens:
        if _is_word_token(token):
            normalized = token.lower().strip("'\"")
        else:
            normalized = None
        entries.append({"original": token, "normalized": normalized})

    # Determine unique candidate words and which are 'hard'
    unique_words = {e['normalized'] for e in entries if e['normalized']}
    hard_words = set()
    for w in unique_words:
        if is_hard_word(w):
            hard_words.add(w)

    # Fetch definitions for hard words in parallel (cached in dictionary_service)
    definitions: Dict[str, Optional[str]] = {}
    if hard_words:
        max_workers = min(10, len(hard_words))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(get_definition, w): w for w in hard_words}
            for fut in concurrent.futures.as_completed(futures):
                w = futures[fut]
                try:
                    definitions[w] = fut.result()
                except Exception:
                    definitions[w] = None

    # Build results mapping back to original tokens
    results = []
    for e in entries:
        norm = e['normalized']
        if norm and norm in hard_words:
            is_hard = True
            definition = definitions.get(norm)
        else:
            is_hard = False
            definition = None

        results.append({
            "word": e['original'],
            "is_hard": is_hard,
            "definition": definition
        })

    return results
