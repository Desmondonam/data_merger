# performs fuzzy matching logic
# fuzzy_merge/fuzzy_matcher.py

from difflib import SequenceMatcher
# from fuzzy_merge.config import LEVENSHTEIN_TOLERANCE
from config import LEVENSHTEIN_TOLERANCE


def levenshtein_ratio(a, b):
    """Calculate the Levenshtein similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()

def is_match(row1, row2):
    """Check if two rows match based on defined criteria."""
    matches = []
    
    # Exact matches
    if row1['zip'] == row2['zip'] and row1['city'] == row2['city']:
        matches.append(True)
    else:
        return False
    
    # Fuzzy matching with Levenshtein distance for other fields
    if levenshtein_ratio(row1['firstname'], row2['firstname']) >= 1 - LEVENSHTEIN_TOLERANCE / len(row1['firstname']):
        matches.append(True)
    if levenshtein_ratio(row1['lastname'], row2['lastname']) >= 1 - LEVENSHTEIN_TOLERANCE / len(row1['lastname']):
        matches.append(True)
    if levenshtein_ratio(row1['street'], row2['street']) >= 1 - LEVENSHTEIN_TOLERANCE / len(row1['street']):
        matches.append(True)
    
    return all(matches)
