# address_matcher/merger.py

import sys
sys.path.append(r'C:\Users\Admin\Desktop\Upwork\Sebastian_Jung\fuzzy_merger')
import pandas as pd
from matcher import FuzzyMatcher
from util import compare_with_regex

class DataMerger:
    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2

    def merge_data(self):
        matcher = FuzzyMatcher(self.df1, self.df2)
        matches = matcher.perform_matching()

        for idx, match in matches.iterrows():
            score = match['similarity_score']
            if score >= matcher.similarity_threshold:
                # Merge data based on highest similarity score match
                matched_row = self.df2.loc[match['match_id']]
                for col in matcher.attributes:
                    if not pd.isna(match[col]) and compare_with_regex(match[col], matched_row[col]):
                        self.df2.at[match['match_id'], col] = match[col]
            else:
                # Add unmatched rows as new entries
                self.df2 = pd.concat([self.df2, self.df1.iloc[[idx]]], ignore_index=True)
        
        return self.df2
