-- EXPLORATORY DATA ANALYSIS

/* Identify top categories (category_name) and top products generating the highest revenue. */
WITH RankedSales AS (
    SELECT 
        c.category_name,
        p.product_title,
        SUM(fs.purchased_last_month * fs.final_price) AS product_revenue,
        ROW_NUMBER() OVER (PARTITION BY c.category_name ORDER BY SUM(fs.purchased_last_month * fs.final_price) DESC) AS ranking
    FROM fact_sales fs
    JOIN dim_categories c ON fs.category_id = c.category_id
    JOIN dim_products p ON fs.product_id = p.product_id
    GROUP BY c.category_id, c.category_name, p.product_id, p.product_title
)
SELECT category_name, product_title, product_revenue
FROM RankedSales
WHERE ranking = 1;

/* Compare the average revenue and review counts between the best-seller group (is_best_seller = 1) 
and the remaining group to evaluate whether this badge truly drives superior performance.*/
SELECT 
    is_best_seller,
    AVG(purchased_last_month * final_price) AS Avg_Revenue, 
    SUM(total_reviews) AS Total_Review_Counts,
    AVG(total_reviews) AS Avg_Review_Counts
FROM 
    fact_sales
GROUP BY 
    is_best_seller;

/* Calculate whether products with discounts (is_discounted = 1) or coupons (has_couponed = 1) 
yield a significantly higher purchase volume (purchased_last_month) compared to full-priced products.*/
SELECT
	is_discounted,
	has_couponed,
    SUM(purchased_last_month) as "purchase volume",
    SUM(purchased_last_month * final_price) as "revenue"
FROM fact_sales
GROUP BY is_discounted, has_couponed;

/* Group ratings into buckets (e.g., <3.0, 3.0-4.0, >4.0) to analyze how review scores influence sales volume.*/
SELECT
	CASE
		WHEN product_rating < 3.0 then "< 3.0"
        WHEN product_rating between 3.0 and 4.0 then "3.0 - 4.0"
        WHEN product_rating > 4.0 then "> 4.0"
    END AS Rating_range,
    sum(purchased_last_month) as "Sales volume"
from fact_sales
group by Rating_range;

/* Detect products with a perfect rating (5.0) but zero or extremely low total_reviews (A sign of clone accounts or new products lacking credibility). */
SELECT product_id, sum(total_reviews)
FROM fact_sales
WHERE product_rating = 5.0 
group by product_id
order by sum(total_reviews) asc;