# # address_matcher/matcher.py

# '''
# An introduction to splink and how it works can be found here: https://pypi.org/project/splink/

# '''
# # address_matcher/matcher.py
# # address_matcher/matcher.py

# import splink.comparison_library as cl
# from splink import Linker, SettingsCreator, block_on
# from config import config
# import pandas as pd

# class FuzzyMatcher:
#     def __init__(self, df1, df2):
#         self.df1 = df1
#         self.df2 = df2
#         self.similarity_threshold = config["similarity_threshold"]
#         self.attributes = config["attributes"]
#         self.linker = None

#     def initialize_linker(self):
#         """Initialize the Splink linker with default DuckDB settings."""
#         self.linker = Linker([self.df1, self.df2])

#     def define_comparisons(self):
#         """Define the fuzzy comparison model using Splink comparison functions."""
#         comparisons = [
#             cl.levenshtein_at_thresholds("email", thresholds=[self.similarity_threshold]),
#             cl.levenshtein_at_thresholds("first_name", thresholds=[self.similarity_threshold]),
#             cl.levenshtein_at_thresholds("last_name", thresholds=[self.similarity_threshold]),
#             cl.jaccard_at_thresholds("street", thresholds=[self.similarity_threshold]),
#             cl.levenshtein_at_thresholds("zip", thresholds=[self.similarity_threshold]),
#             cl.jaccard_at_thresholds("city", thresholds=[self.similarity_threshold]),
#         ]
#         return comparisons

#     def perform_matching(self):
#         """Perform fuzzy matching using Splink on the specified attributes."""
#         self.initialize_linker()
        
#         # Set up model settings
#         settings = SettingsCreator(
#             comparisons=self.define_comparisons(),
#             blocking_rules=block_on("zip"),
#             unique_id_column_name="id"
#         )
        
#         # Add settings to linker
#         self.linker.compute_comparison_vector_table(settings)
        
#         # Find matches with similarity scores above the threshold
#         results = self.linker.predict()
#         matches = results[results["match_probability"] >= self.similarity_threshold]
        
#         return matches


import pandas as pd
from rapidfuzz import fuzz

class FuzzyMatcher:
    def __init__(self, df1, df2, similarity_threshold=80):
        """
        Initialize the FuzzyMatcher with two DataFrames and a similarity threshold.

        :param df1: First DataFrame
        :param df2: Second DataFrame
        :param similarity_threshold: Similarity score threshold (default: 80)
        """
        self.df1 = df1
        self.df2 = df2
        self.similarity_threshold = similarity_threshold
        self.attributes = ["email", "first_name", "last_name", "street", "zip", "city"]  # Hardcoded attributes for comparison

    def compute_similarity(self, str1, str2, method='ratio'):
        """
        Compute similarity between two strings using rapidfuzz.

        :param str1: First string
        :param str2: Second string
        :param method: Similarity calculation method ('ratio', 'partial_ratio', etc.)
        :return: Similarity score
        """
        if pd.isna(str1) or pd.isna(str2):
            return 0

        methods = {
            'ratio': fuzz.ratio,
            'partial_ratio': fuzz.partial_ratio,
            'token_sort_ratio': fuzz.token_sort_ratio,
            'token_set_ratio': fuzz.token_set_ratio
        }
        return methods[method](str1, str2)

    def perform_matching(self):
        """
        Perform fuzzy matching between two DataFrames.

        :return: DataFrame of matches with similarity scores
        """
        matches = []

        for idx1, row1 in self.df1.iterrows():
            for idx2, row2 in self.df2.iterrows():
                match_data = {"df1_id": idx1, "df2_id": idx2, "similarity_score": 0}
                for attr in self.attributes:
                    if attr in self.df1.columns and attr in self.df2.columns:
                        similarity = self.compute_similarity(row1[attr], row2[attr])
                        match_data[attr + "_similarity"] = similarity
                        match_data["similarity_score"] += similarity
                match_data["similarity_score"] /= len(self.attributes)  # Average score
                if match_data["similarity_score"] >= self.similarity_threshold:
                    matches.append(match_data)

        return pd.DataFrame(matches)