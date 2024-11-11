import pandas as pd
from fuzzy_matcher import is_match
from config import COLUMNS_TO_COMPARE

def merge_data(df1, df2):
    """Merge data from df1 into df2 based on exact row-wise matching criteria."""
    
    for _, row1 in df1.iterrows():
        match_found = False

        # Iterate over rows in df2 to check for an exact row-wise match across specified columns
        for _, row2 in df2.iterrows():
            # Check if the entire row matches across COLUMNS_TO_COMPARE
            if all(row1[col] == row2[col] for col in COLUMNS_TO_COMPARE):
                match_found = True
                break
        
        # If no exact match is found, add the new row from df1 to df2
        if not match_found:
            df2 = pd.concat([df2, row1.to_frame().T], ignore_index=True)
    
    return df2
