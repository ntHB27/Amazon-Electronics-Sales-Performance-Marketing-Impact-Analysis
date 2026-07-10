import pandas as pd
import scipy.stats as stats
import urllib.parse
from sqlalchemy import create_engine
import os
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

print(f"Load success {df.shape[0]} rows and {df.shape[1]} coulmns!")

print("BQ2 ANALYSIS: BEST SELLER CHARACTERISTICS")

# split data into 2 groups
best_seller_df = df[df['is_best_seller'] == True]
normal_df = df[df['is_best_seller'] == False]

print(f"Number of Best Sellers: {len(best_seller_df)}")
print(f"Number of Normal Products: {len(normal_df)}\n")

# Use Mann-Whitney U test 
def run_mann_whitney(feature_name, feature_desc):
    # Calculate medians for both groups
    median_bs = best_seller_df[feature_name].median()
    median_normal = normal_df[feature_name].median()
    
    # alternative='two-sided' 
    stat, p_value = stats.mannwhitneyu(
        best_seller_df[feature_name].dropna(), 
        normal_df[feature_name].dropna(), 
        alternative='two-sided'
    )
    
    print(f"--- Comparing {feature_desc} ({feature_name}) ---")
    print(f"Median (Best Seller): {median_bs}")
    print(f"Median (Normal)     : {median_normal}")
    print(f"P-value             : {p_value}")
    
    if p_value < 0.05:
        print("=> Statistically significant difference between the two groups.\n")
    else:
        print("=> No statistically significant difference between the two groups.\n")

run_mann_whitney('final_price', 'Final Price')
run_mann_whitney('total_reviews', 'Total Reviews')