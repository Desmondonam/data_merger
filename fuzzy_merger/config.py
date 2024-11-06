# Configurations for the matching criteria
# fuzzy_merge/config.py

MATCH_THRESHOLD = 0.95  # Minimum score for a match to be considered valid
COLUMNS_TO_COMPARE = ["email", "firstname", "lastname", "street", "zip", "city"]
LEVENSHTEIN_TOLERANCE = 2  # Max edit distance for names and addresses
