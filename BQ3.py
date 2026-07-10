import os
import urllib.parse
import pandas as pd
import scipy.stats as stats
from sqlalchemy import create_engine
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv(dotenv_path='connect.env')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_NAME')

encoded_password = urllib.parse.quote_plus(password)
db_connection_str = f'mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database}'
engine = create_engine(db_connection_str)
# query to fetch data from the database
query = "SELECT * FROM fact_sales" 
df = pd.read_sql(query, engine)

print(f"Successfully loaded {df.shape[0]} rows and {df.shape[1]} columns!\n")

print("BQ3 ANALYSIS: MARKETING FLAGS IMPACT")

df['is_promoted'] = (df['has_couponed'] == True) | (df['is_discounted'] == True)

promoted_df = df[df['is_promoted'] == True]
full_price_df = df[df['is_promoted'] == False]

print(f"Number of Promoted Products: {len(promoted_df)}")
print(f"Number of Full Price Products: {len(full_price_df)}\n")

# calculate medians for both groups
median_promoted = promoted_df['purchased_last_month'].median()
median_full_price = full_price_df['purchased_last_month'].median()

# Use Mann-Whitney U test to compare sales volume between promoted and full price products
stat, p_value = stats.mannwhitneyu(
    promoted_df['purchased_last_month'].dropna(), 
    full_price_df['purchased_last_month'].dropna(), 
    alternative='two-sided'
)

# print results
print("--- Comparing Sales Volume (purchased_last_month) ---")
print(f"Median (Promoted)  : {median_promoted}")
print(f"Median (Full Price): {median_full_price}")
print(f"P-value            : {p_value}")

if p_value < 0.05:
    print("=> Statistically significant difference in sales volume between groups.\n")
else:
    print("=> No statistically significant difference in sales volume between groups.\n")