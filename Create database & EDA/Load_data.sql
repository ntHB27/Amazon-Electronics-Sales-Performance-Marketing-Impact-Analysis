SET SESSION sql_mode = '';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_data.csv' 
INTO TABLE staging_amazon
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

INSERT INTO Dim_Categories (category_name)
SELECT DISTINCT Category 
FROM staging_amazon
WHERE Category IS NOT NULL AND Category != '';

INSERT INTO Dim_Products (product_title)
SELECT DISTINCT product_title 
FROM staging_amazon
WHERE product_title IS NOT NULL;

SET SQL_SAFE_UPDATES = 0;

UPDATE staging_amazon sa
JOIN Dim_Categories dc ON sa.Category = dc.category_name
SET sa.temp_category_id = dc.category_id;

UPDATE staging_amazon sa
JOIN Dim_Products dp ON sa.product_title = dp.product_title
SET sa.temp_product_id = dp.product_id;

SET SQL_SAFE_UPDATES = 1;

-- Đổ dữ liệu tổng hợp đã có sẵn ID SỐ vào Fact_Sales 
INSERT INTO Fact_Sales (
    product_id, 
    category_id, 
    product_rating, 
    total_reviews, 
    purchased_last_month, 
    final_price, 
    is_best_seller, 
    is_sponsored, 
    has_couponed, 
    is_discounted, 
    buy_box_availability
)
SELECT 
    sa.temp_product_id,
    sa.temp_category_id,
    sa.product_rating,
    sa.total_reviews,
    CAST(sa.purchased_last_month AS UNSIGNED),
    sa.final_price,
    CASE WHEN TRIM(sa.is_best_seller) = 'True' THEN 1 ELSE 0 END,
    CASE WHEN TRIM(sa.is_sponsored) = 'True' THEN 1 ELSE 0 END,
    CASE WHEN TRIM(sa.has_couponed) = 'True' THEN 1 ELSE 0 END,
    CASE WHEN TRIM(sa.is_discounted) = 'True' THEN 1 ELSE 0 END,
    sa.buy_box_availability
FROM staging_amazon sa;

DROP TABLE staging_amazon;
