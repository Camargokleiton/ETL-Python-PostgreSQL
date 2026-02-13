import pandas as pd

# Functions to save DataFrame in various formats
def save_to_csv(df, file_path): 
    df.to_csv(file_path, index=False)
    
def save_to_excel(df, file_path):
    df.to_excel(file_path, index=False)

def save_to_parquet(df, file_path):
    df.to_parquet(file_path, index=False)

def save_to_json(df, file_path):
    df.to_json(file_path, orient='records', lines=True)

def save_to_sql(df, table_name, connection):
    df.to_sql(table_name, con=connection, if_exists='replace', index=False)

def save_to_pickle(df, file_path):
    df.to_pickle(file_path) 
    
def save_to_hdf(df, file_path, key='data'):
    df.to_hdf(file_path, key=key, mode='w')

def save_to_feather(df, file_path):
    df.to_feather(file_path)

def save_to_csv_gz(df, file_path):
    df.to_csv(file_path, index=False, compression='gzip')