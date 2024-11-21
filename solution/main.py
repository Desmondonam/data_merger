import pandas as pd
import logging
from Levenshtein import ratio  # Install via pip: pip install python-Levenshtein


class FuzzyMatcher:
    """Handles fuzzy matching of records using custom logic."""
    
    def __init__(self, df1, df2, similarity_threshold=0.95):
        self.df1 = df1.copy()
        self.df2 = df2.copy()
        self.similarity_threshold = similarity_threshold
        self.attributes = ['email', 'first_name', 'last_name', 'street', 'zip', 'city']
        self._validate_dataframes()
        self._setup_logger()
        
    def _setup_logger(self):
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _validate_dataframes(self):
        required_columns = set(self.attributes)
        df1_columns = set(self.df1.columns)
        df2_columns = set(self.df2.columns)
        
        if not required_columns.issubset(df1_columns):
            missing = required_columns - df1_columns
            raise ValueError(f"First dataframe missing required columns: {missing}")
            
        if not required_columns.issubset(df2_columns):
            missing = required_columns - df2_columns
            raise ValueError(f"Second dataframe missing required columns: {missing}")
    
    def _calculate_similarity(self, value1, value2):
        if pd.isna(value1) or pd.isna(value2):
            return 0.0
        return ratio(str(value1).lower(), str(value2).lower())
    
    def _compare_records(self, record1, record2):
        similarities = [
            self._calculate_similarity(record1[attr], record2[attr])
            for attr in self.attributes
        ]
        return sum(similarities) / len(similarities)
    
    def _block_records(self):
        self.logger.info("Performing blocking...")
        df1_blocked = self.df1.set_index('zip')
        df2_blocked = self.df2.set_index('zip')
        
        common_zips = df1_blocked.index.intersection(df2_blocked.index)
        
        candidates = []
        for zip_code in common_zips:
            df1_candidates = df1_blocked.loc[[zip_code]].reset_index()
            df2_candidates = df2_blocked.loc[[zip_code]].reset_index()
            for _, record1 in df1_candidates.iterrows():
                for _, record2 in df2_candidates.iterrows():
                    candidates.append((record1, record2))
        
        self.logger.info(f"Generated {len(candidates)} candidate pairs from blocking.")
        return candidates
    
    def perform_matching(self):
        self.logger.info("Starting fuzzy matching process...")
        
        candidate_pairs = self._block_records()
        
        matches = []
        for record1, record2 in candidate_pairs:
            similarity = self._compare_records(record1, record2)
            if similarity >= self.similarity_threshold:
                matches.append({
                    'df1_index': record1.name,
                    'df2_index': record2.name,
                    'similarity': similarity
                })
        
        matches_df = pd.DataFrame(matches)
        self.logger.info(f"Found {len(matches_df)} matches above threshold {self.similarity_threshold}.")
        return matches_df

def update_df2_based_on_matches(df1, df2, matches_df):
    """
    Updates df2 with new records from df1 based on matching results.
    If a match exists, updates the record in df2.
    If no match exists, appends the new record to df2.
    
    Args:
        df1 (pd.DataFrame): The first dataframe (source of updates).
        df2 (pd.DataFrame): The second dataframe (target for updates).
        matches_df (pd.DataFrame): Matching results with indices of matched rows and similarity scores.
    
    Returns:
        pd.DataFrame: The updated version of df2.
    """
    # Iterate over each match and update df2 with values from df1
    for _, match in matches_df.iterrows():
        df1_index = match['df1_index']
        df2_index = match['df2_index']

        # Update df2 row with df1 values for the matching row
        df2.loc[df2_index] = df1.loc[df1_index]

    # Find records in df1 that did not match with df2
    unmatched_df1_indices = list(set(df1.index) - set(matches_df['df1_index']))  # Convert set to list
    unmatched_df1 = df1.loc[unmatched_df1_indices]

    # Append unmatched records to df2
    df2 = pd.concat([df2, unmatched_df1], ignore_index=True)
    
    return df2

# Example Usage
if __name__ == "__main__":
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

    matcher = FuzzyMatcher(df1, df2, similarity_threshold=0.85)
    matches = matcher.perform_matching()
    updated_df2 = update_df2_based_on_matches(df1, df2, matches)
    print("Updated df2:")
    print(updated_df2)
