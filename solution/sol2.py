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


# Example Usage
if __name__ == "__main__":
    df1 = pd.DataFrame({
        'email': ['test@example.com', 'john.doe@gmail.com'],
        'first_name': ['Test', 'John'],
        'last_name': ['User', 'Doe'],
        'street': ['123 Elm St', '456 Maple Ave'],
        'zip': ['12345', '67890'],
        'city': ['Springfield', 'Metropolis']
    })

    df2 = pd.DataFrame({
        'email': ['test@example.com', 'jane.doe@gmail.com'],
        'first_name': ['Test', 'Jane'],
        'last_name': ['User', 'Doe'],
        'street': ['123 Elm St', '789 Oak St'],
        'zip': ['12345', '67890'],
        'city': ['Springfield', 'Gotham']
    })

    matcher = FuzzyMatcher(df1, df2, similarity_threshold=0.85)
    matches = matcher.perform_matching()
    print(matches)
    print(df2)
