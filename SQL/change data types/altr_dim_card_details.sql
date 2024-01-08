-- Update card_number column
ALTER TABLE dim_card_details ALTER COLUMN card_number TYPE VARCHAR(20);

-- Update expiry_date column
ALTER TABLE dim_card_details ALTER COLUMN expiry_date TYPE VARCHAR(20);

-- Update date_payment_confirmed column
ALTER TABLE dim_card_details ALTER COLUMN date_payment_confirmed TYPE DATE USING (CAST(date_payment_confirmed AS DATE));