ALTER TABLE dim_users
ALTER COLUMN first_name TYPE VARCHAR(20);

-- Change last_name to VARCHAR with a maximum length
ALTER TABLE dim_users
ALTER COLUMN last_name TYPE VARCHAR(20);

-- Change date_of_birth to DATE
ALTER TABLE dim_users
ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::DATE;

-- Change country_code to VARCHAR with a maximum length
ALTER TABLE dim_users
ALTER COLUMN country_code TYPE VARCHAR(20);

-- Change user_uuid to UUID
ALTER TABLE dim_users
ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID;

-- Change join_date to DATE
ALTER TABLE dim_users
ALTER COLUMN join_date TYPE DATE USING join_date::DATE;
