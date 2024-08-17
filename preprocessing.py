import pandas as pd

def clean_party_affiliation(df):
    filtered_df = df[df['Party Affiliation'].isin(['Democratic', 'Republican'])]
    return filtered_df

def clean_sentence_count(df):
    filtered_df = df[df['Sentence Count'] >= 10]
    return filtered_df

senators_df = pd.read_csv('Databases/senators_info.csv', index_col=0, header=0)
senators_party_df = clean_party_affiliation(senators_df)
filtered_senators_df = clean_sentence_count(senators_party_df)
filtered_senators_df.to_csv('Databases/final_senators_info.csv', index=False)

representatives_df = pd.read_csv('Databases/representatives_info.csv', index_col = 0, header=0)
representatives_party_df = clean_party_affiliation(representatives_df)
filtered_representatives_df = clean_sentence_count(representatives_party_df)
filtered_representatives_df.to_csv('Databases/final_representatives_info.csv', index=False)

politicians_df = pd.concat([filtered_senators_df, filtered_representatives_df], ignore_index=True)
politicians_df.to_csv('Databases/final_politicians_info.csv', index=False)
