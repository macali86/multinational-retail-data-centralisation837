-- Change date_uuid to UUID
ALTER TABLE orders_table
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;

-- Change user_uuid to UUID
ALTER TABLE orders_table
ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID;

-- Change card_number to VARCHAR with a maximum length
ALTER TABLE orders_table
ALTER COLUMN card_number TYPE VARCHAR(20);

-- Change store_code to VARCHAR with a maximum length
ALTER TABLE orders_table
ALTER COLUMN store_code TYPE VARCHAR(15);

-- Change product_code to VARCHAR with a maximum length
ALTER TABLE orders_table
ALTER COLUMN product_code TYPE VARCHAR(15);

-- Change product_quantity to SMALLINT
ALTER TABLE orders_table
ALTER COLUMN product_quantity TYPE SMALLINT;
