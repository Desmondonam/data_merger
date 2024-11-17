# address_matcher/utils.py

import re

def compare_with_regex(value1, value2):
    """Compare two values using regex for possible variations."""
    pattern = re.compile(re.escape(value1), re.IGNORECASE)
    return bool(pattern.fullmatch(value2)) or bool(pattern.fullmatch(value1))
