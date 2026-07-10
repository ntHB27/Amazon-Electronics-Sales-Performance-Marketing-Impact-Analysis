CREATE DATABASE amazon_sales_db;
USE amazon_sales_db;

-- 1. Create Dim_Categories
CREATE TABLE Dim_Categories (
    category_id INT NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (category_id),
    INDEX idx_category_name (category_name) 
);

-- 2. Create Dim_Products
CREATE TABLE Dim_Products (
    product_id INT NOT NULL AUTO_INCREMENT,
    product_title VARCHAR(500) NOT NULL, 
    PRIMARY KEY (product_id),
    INDEX idx_product_title (product_title(255)) 
);

-- 3. Create Fact_Sales
CREATE TABLE Fact_Sales (
    fact_id BIGINT NOT NULL AUTO_INCREMENT,
    product_id INT,
    category_id INT,
    product_rating DECIMAL(3,1),
    total_reviews INT,
    purchased_last_month INT,
    final_price DECIMAL(10,2),
    is_best_seller TINYINT(1), 
    is_sponsored TINYINT(1),
    has_couponed TINYINT(1),
    is_discounted TINYINT(1),
    buy_box_availability VARCHAR(100),
    PRIMARY KEY (fact_id),
    FOREIGN KEY (product_id) REFERENCES Dim_Products(product_id),
    FOREIGN KEY (category_id) REFERENCES Dim_Categories(category_id)
) ENGINE=InnoDB;

CREATE TABLE staging_amazon (
    product_title VARCHAR(500), 
    product_rating DECIMAL(3,1),
    total_reviews INT,
    purchased_last_month DECIMAL(10,2), 
    is_best_seller VARCHAR(10),         
    is_sponsored VARCHAR(10),
    has_couponed VARCHAR(10),
    buy_box_availability VARCHAR(100),
    final_price DECIMAL(10,2),
    is_discounted VARCHAR(10),
    Category VARCHAR(255),
    temp_product_id INT,   
    temp_category_id INT,  
    INDEX idx_stage_title (product_title(255)), 
    INDEX idx_stage_cat (Category)              
);