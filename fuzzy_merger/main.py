# main entry point for the solution
# fuzzy_merge/main.py

import pandas as pd
# from fuzzy_merge.data_merger import merge_data
from data_merger import merge_data


# Sample data
data1 = {
    'email': ['john.doe@example.com', 'jane.smith@example.com'],
    'firstname': ['John', 'Jane'],
    'lastname': ['Doe', 'Smith'],
    'street': ['123 Maple Street', '456 Oak Avenue'],
    'zip': ['12345', '67890'],
    'city': ['Metropolis', 'Gotham']
}

data2 = {
    'email': ['john.d@example.com', 'jane.s@example.com'],
    'firstname': ['Jon', 'Janie'],
    'lastname': ['Do', 'Smith'],
    'street': ['123 Maple St', '456 Oak Ave'],
    'zip': ['12345', '67890'],
    'city': ['Metropolis', 'Gotham']
}

# Convert to DataFrames
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Perform the merge
df2 = merge_data(df1, df2)

print("Updated DataFrame 2:")
print(df2)
