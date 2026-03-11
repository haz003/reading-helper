from typing import Optional
import requests
from functools import lru_cache


@lru_cache(maxsize=2048)
def _fetch_definition(clean_word: str) -> Optional[str]:
    """Fetch definition from the remote API for a cleaned, lowercase word.

    This internal function is cached with `lru_cache` to avoid repeated
    network calls for the same word.
    """
    URL = f"https://api.dictionaryapi.dev/api/v2/entries/en/{clean_word}"
    try:
        r = requests.get(url=URL, timeout=5)
    except requests.RequestException:
        return None

    if r.status_code == 404:
        return None

    try:
        return r.json()[0]['meanings'][0]['definitions'][0]['definition']
    except Exception:
        return None


def get_definition(word: str) -> Optional[str]:
    """Public wrapper: clean input then call cached fetcher.

    Returns a string definition or None when unavailable.
    """
    clean_word = word.lower().strip(".,!?;:\'\"")
    if not clean_word:
        return None
    return _fetch_definition(clean_word)