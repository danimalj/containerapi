select * from my_table;

-- Insert 10 records into the table
INSERT INTO my_table (text_field)
VALUES
    ('First record'),
    ('Second record'),
    ('Third record'),
    ('Fourth record'),
    ('Fifth record'),
    ('Sixth record'),
    ('Seventh record'),
    ('Eighth record'),
    ('Ninth record'),
    ('Tenth record');

commit;

-- Update every other record in the table
WITH ranked_records AS (
    SELECT id, ROW_NUMBER() OVER () AS row_num
    FROM my_table
)
UPDATE my_table
SET 
    updated_at = current_timestamp,
    updated_by = current_user,
    text_field = CONCAT(text_field, ' (Updated)')
WHERE id IN (
    SELECT id 
    FROM ranked_records
    WHERE row_num % 2 = 0
);

commit;