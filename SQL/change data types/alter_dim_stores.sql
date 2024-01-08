ALTER TABLE dim_store_details
ALTER COLUMN longitude TYPE FLOAT USING longitude::FLOAT;

ALTER TABLE dim_store_details
ALTER COLUMN locality TYPE VARCHAR(255);

ALTER TABLE dim_store_details
ALTER COLUMN store_code TYPE VARCHAR(50);

ALTER TABLE dim_store_details
ALTER COLUMN staff_numbers TYPE SMALLINT;

ALTER TABLE dim_store_details
ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE;

ALTER TABLE dim_store_details
ALTER COLUMN store_type TYPE VARCHAR(255);

ALTER TABLE dim_store_details
ALTER COLUMN latitude TYPE FLOAT USING latitude::FLOAT;

ALTER TABLE dim_store_details
ALTER COLUMN country_code TYPE VARCHAR(50);

ALTER TABLE dim_store_details
ALTER COLUMN continent TYPE VARCHAR(255);