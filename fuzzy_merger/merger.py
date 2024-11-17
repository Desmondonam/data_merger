import sys
sys.path.append(r'C:\Users\Admin\Desktop\Upwork\Sebastian_Jung\fuzzy_merger')
import pandas as pd
from matcher import FuzzyMatcher
from util import compare_with_regex

class DataMerger:
    def __init__(self, df1, df2):
        self.df1 = df1.reset_index(drop=True)  # Reset index for consistency
        self.df2 = df2.reset_index(drop=True)

    def merge_data(self):
        matcher = FuzzyMatcher(self.df1, self.df2)
        matches = matcher.perform_matching()

        matched_indices = set()  # To track rows that have been matched

        for idx, match in matches.iterrows():
            score = match['similarity_score']
            if score >= matcher.similarity_threshold:
                # Process matching rows
                matched_row = self.df2.loc[match['match_id']]
                matched_indices.add(match['match_id'])

                for col in matcher.attributes:
                    # Merge attributes based on regex and non-null conditions
                    if not pd.isna(match[col]) and compare_with_regex(match[col], matched_row[col]):
                        self.df2.at[match['match_id'], col] = match[col]
            else:
                # Keep track of unmatched rows
                print(f"Low similarity score: {score} for row {idx}")

        # Add unmatched rows from df1 to df2
        unmatched_rows = self.df1.loc[~self.df1.index.isin(matched_indices)]
        if not unmatched_rows.empty:
            print(f"Adding unmatched rows to df2:\n{unmatched_rows}")
            self.df2 = pd.concat([self.df2, unmatched_rows], ignore_index=True)

        return self.df2
