# Amazon-Electronics-Sales-Performance-Marketing-Impact-Analysis
Personal project

# Amazon Electronics Sales Performance & Marketing Impact Analysis

## 1. Project Overview
In a highly competitive e-commerce environment, understanding what drives product sales performance is critical. While factors such as pricing and product quality are often considered, the quantitative impact of marketing strategies (e.g., sponsorships, coupons, and best-seller labels) remains unclear.

This project aims to identify and quantify the key factors influencing Amazon electronics product sales. It focuses on evaluating the effectiveness of marketing strategies alongside pricing and product-related attributes using exploratory data analysis (EDA), statistical hypothesis testing, and interactive dashboarding.

## 2. Tech Stack & Data Architecture
* **Data Source:** Amazon Electronics Sales Dataset (~37,000 records).
* **Data Processing & Stats:** Python (Pandas, SciPy, Matplotlib/Seaborn).
* **Database & Ingestion:** MySQL (Configured secure `.env` connection for dynamic querying).
* **BI & Visualization:** PowerBI (Advanced DAX, Interactive Slicers, Cross-table filtering).
* **Key Techniques:** Feature Engineering (Extracting structured category data from unstructured product titles), Non-parametric Statistical Testing (Mann-Whitney U Test), Data Storytelling.

## 3. Key Business Questions & Findings

### BQ1 - Price Sweet Spots
* **Question:** Which price segments drive the highest purchasing volume within the Top 5 Categories?
* **Approach:** Segmented the market into 5 independent Price Tiers (Quintiles) for each category using DAX percentile functions.
* **Key Finding:** The highest sales volume consistently falls within Tier 1 (Cheapest) and Tier 2. For example, the optimal price range for the *Chargers & Cables* category was identified exactly between $10.50 - $14.99.

### BQ2 - Best Seller Profiling
* **Question:** How do the structural characteristics (specifically price and total reviews) of "Best Seller" products differ from the rest of the market? 
* **Approach:** Conducted a Mann-Whitney U test to prove statistical significance.
* **Key Finding (P-value < 0.05):** Best Sellers are structurally different. They rely heavily on a massive "social proof" moat (Median: 8,449 reviews vs. 335 for normal products) and compete aggressively on pricing (Median: $39.99 vs. $89.99).

### BQ3 - Marketing Flags Impact
* **Question:** From a macro-market perspective, do listings with promotional flags (`has_couponed` / `is_discounted`) generate a significantly higher sales volume compared to full-price products?
* **Approach:** Binary grouping (Promoted vs. Full Price) evaluated via Mann-Whitney U Test.
* **Key Finding (P-value = 0.0):** Promotions are the market norm (~76% of products use them). Applying a marketing flag mathematically doubles the sales velocity (Median volume of 100 units/month vs. 50 units/month for full-price items).

## 📊 4. Interactive PowerBI Dashboard
*(Provide a brief description of how stakeholders can use the dashboard here)*

![Dashboard Overview](results/dashboard_overview.png)

![Price Sweet Spot Matrix](results/sweet_spot_matrix.png)


## 5. Future Work & Limitations
* **Addressing Data Imbalance:** The dataset shows an imbalance in certain marketing features, particularly coupon availability. To mitigate potential bias, future iterations will supplement the current A/B testing approach with multiple regression analysis.
* **Fraud Detection Pipeline:** Plan to implement an anomaly detection script to flag "Spam" / Fake Products (e.g., items boasting a perfect 5.0 rating but possessing zero or extremely low `total_reviews`, indicating clone accounts).
