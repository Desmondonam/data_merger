# Handles merging logic and updates
# fuzzy_merge/data_merger.py

import pandas as pd
# from fuzzy_merge.fuzzy_matcher import is_match
# from fuzzy_merge.config import COLUMNS_TO_COMPARE

from fuzzy_matcher import is_match
from config import COLUMNS_TO_COMPARE

def merge_data(df1, df2):
    """Merge data from df1 into df2 based on fuzzy matching criteria."""
    
    for _, row1 in df1.iterrows():
        match_found = False
        
        for _, row2 in df2.iterrows():
            if is_match(row1, row2):
                match_found = True
                for col in COLUMNS_TO_COMPARE:
                    if pd.isna(row2[col]):
                        df2.loc[row2.name, col] = row1[col]
                break

        # If no match is found, add new row from df1 to df2
        if not match_found:
            df2 = pd.concat([df2, row1.to_frame().T], ignore_index=True)
    
    return df2
