SELECT
    dim_store_details.store_type,
    SUM(product_quantity * dim_products.product_price) AS total_sales,
    ROUND(CAST(100 * SUM(product_quantity * dim_products.product_price) AS DECIMAL(14, 2)) /
       CAST((SELECT SUM(product_quantity * dim_products.product_price)
              FROM orders_table JOIN dim_products ON orders_table.product_code = dim_products.product_code) AS DECIMAL(10, 2)), 2) AS percentage_total
FROM orders_table
JOIN dim_products ON orders_table.product_code = dim_products.product_code
JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY dim_store_details.store_type
ORDER BY total_sales DESC;

