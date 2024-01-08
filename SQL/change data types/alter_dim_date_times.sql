-- Update month column
ALTER TABLE dim_date_times ALTER COLUMN month TYPE VARCHAR(2);

-- Update year column
ALTER TABLE dim_date_times ALTER COLUMN year TYPE VARCHAR(4);

-- Update day column
ALTER TABLE dim_date_times ALTER COLUMN day TYPE VARCHAR(2);

-- Update time_period column
ALTER TABLE dim_date_times ALTER COLUMN time_period TYPE VARCHAR(55);

-- Update date_uuid column
ALTER TABLE dim_date_times ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid;
