-- Rename the "removed" column to "still_available"
ALTER TABLE dim_products
RENAME COLUMN removed TO still_available;

-- Change data types of the columns
ALTER TABLE dim_products
ALTER COLUMN product_price TYPE FLOAT USING product_price::DOUBLE PRECISION,
ALTER COLUMN weight TYPE FLOAT USING weight::DOUBLE PRECISION,
ALTER COLUMN EAN TYPE VARCHAR(13),
ALTER COLUMN product_code TYPE VARCHAR(20),
ALTER COLUMN date_added TYPE DATE,
ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
ALTER COLUMN still_available TYPE BOOLEAN USING still_available::BOOLEAN,
ALTER COLUMN weight_class TYPE VARCHAR(25);
