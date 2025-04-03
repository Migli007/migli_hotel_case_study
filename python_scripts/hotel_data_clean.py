import pandas as pd
from sqlalchemy import create_engine

excel_file = r"C:\Users\migli\OneDrive\Desktop\ihg_file\ihg_data.xlsx"


df = pd.read_excel(excel_file, sheet_name='METRICS')  

# duplicates checking
if df.duplicated().sum() > 0:
    print(f"There are {df.duplicated().sum()} duplicate rows.")
else:
    print("No duplicate rows found.")

# negative number checking
numeric_cols = df.select_dtypes(include=['number']).columns
negative_values = (df[numeric_cols] < 0).any().sum()

if negative_values > 0:
    print("There are negative values in the following columns:")
    print(df[numeric_cols].lt(0).any())

# Remove duplicates
df = df.drop_duplicates()

engine = create_engine('postgresql://postgres:%40Supermanredson1@localhost:5432/ihg_test')

df.to_sql('metrics', engine, if_exists='replace', index=False)

print("Upload successful!")
