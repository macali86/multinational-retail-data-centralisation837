UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '');

-- Add the new column weight_class
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(50);

-- Update weight_class based on weight range
UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
    WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
    WHEN weight >= 140 THEN 'Truck_Required'
    ELSE NULL -- Handle any other cases
END;

