import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
query = "SELECT c.category_name, purchased_last_month, final_price FROM fact_sales fs JOIN dim_categories c ON fs.category_id = c.category_id " 
df = pd.read_sql(query, engine)

print(f"Load success {df.shape[0]} rows and {df.shape[1]} coulmns!")

sns.set_theme(style="whitegrid")
# find top 5 categories with the highest market volume
top_categories = df.groupby('category_name')['purchased_last_month'].sum().nlargest(5).index.tolist()
print(f"\n Top 5 Categories: {top_categories}\n")
df_top_cats = df[df['category_name'].isin(top_categories)].copy()

# create price tiers for each category using quantiles
def assign_price_tier(group):
    return pd.qcut(group, q=5, labels=['Tier 1 (Cheapest)', 'Tier 2', 'Tier 3', 'Tier 4', 'Tier 5'], duplicates='drop')

df_top_cats['price_tier'] = df_top_cats.groupby('category_name')['final_price'].transform(assign_price_tier)

# find sweet spot
sweet_spot_df = df_top_cats.groupby(['category_name', 'price_tier'], observed=False)['purchased_last_month'].median().reset_index()

plt.figure(figsize=(14, 6))
sns.barplot(data=sweet_spot_df, x='category_name', y='purchased_last_month', hue='price_tier', palette='viridis')

plt.title('BQ1: Price Sweet Spots - Median Sales Volume by Price Tiers (Top 5 Categories)', fontsize=14, fontweight='bold')
plt.ylabel('Median Units Purchased (Last Month)')
plt.xlabel('category_name')
plt.legend(title='Price Tier', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# calculate price ranges for each tier
price_ranges = df_top_cats.groupby(['category_name', 'price_tier'], observed=False)['final_price'].agg(['min', 'max']).reset_index()
price_ranges['price_range'] = "$" + price_ranges['min'].round(2).astype(str) + " - $" + price_ranges['max'].round(2).astype(str)
price_pivot = price_ranges.pivot(index='category_name', columns='price_tier', values='price_range')
print("\n PRICE RANGES FOR EACH TIER:\n")
print(price_pivot)
print("-" * 60)