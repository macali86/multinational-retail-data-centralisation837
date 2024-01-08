SELECT
  SUM(CASE WHEN store_code = 'WEB-1388012W' THEN 1 ELSE 0 END) AS numbers_of_sales,
  SUM(product_quantity) AS product_quantity_count,
  MAX(CASE WHEN store_code = 'WEB-1388012W' THEN 'Web' ELSE 'Offline' END) AS location,
  SUM(product_quantity * dim_products.product_price) AS total_sales_amount
FROM orders_table
JOIN dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY store_code = 'WEB-1388012W';
