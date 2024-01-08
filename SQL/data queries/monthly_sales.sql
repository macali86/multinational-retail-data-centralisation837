SELECT
    month,
    SUM(product_quantity * product_price) AS total_sales
FROM dim_date_times
JOIN orders_table ON dim_date_times.date_uuid = orders_table.date_uuid
JOIN dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY month
ORDER BY total_sales DESC;
