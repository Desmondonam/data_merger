import sys
sys.path.append('C:/Users/Admin/Desktop/Upwork/Sebastian_Jung/fuzzy_merger/')
import pandas as pd
import util
from util import compare_with_regex
import matcher
from matcher import FuzzyMatcher # , DataMerger
data1 = {
    'email': ['john.doe@example.com', 'jane.smith@example.com'],
    'first_name': ['John', 'Jane'],
    'last_name': ['Doe', 'Smith'],
    'street': ['123 Maple St', '456 Oak St'],
    'zip': ['12345', '67890'],
    'city': ['Springfield', 'Shelbyville']
}

data2 = {
    'email': ['jane.smith@example.com', 'john.doe@example.com'],
    'first_name': ['Jane', 'John'],
    'last_name': ['Smith', 'Doe'],
    'street': ['456 Oak Street', '123 Maple Street'],
    'zip': ['67890', '12345'],
    'city': ['Shelbyville', 'Springfield']
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

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
    
merger = DataMerger(df1, df2)
merged_df = merger.merge_data()

    # Step 5: Display the results
print("Merged DataFrame:")
print(merged_df)