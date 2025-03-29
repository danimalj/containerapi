-- Create the tablespace
CREATE TABLESPACE other LOCATION '/var/lib/postgresql/data';

-- Create the table
CREATE TABLE my_table (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    text_field TEXT,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL, -- Updated default value
    updated_by TEXT
) TABLESPACE other;

-- Function to set 'updated_at' and 'updated_by' on INSERT or UPDATE
CREATE OR REPLACE FUNCTION modify_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    -- On INSERT: Set 'updated_at' and 'updated_by'
    IF TG_OP = 'INSERT' THEN
        NEW.updated_by = current_user;      -- Set updated_by to the current user
    END IF;

    -- On UPDATE: Update 'updated_at' and 'updated_by'
    IF TG_OP = 'UPDATE' THEN
        NEW.updated_at = current_timestamp; -- Update the timestamp
        NEW.updated_by = current_user;      -- Update the user
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for UPDATE operations
CREATE TRIGGER update_trigger
BEFORE UPDATE ON my_table
FOR EACH ROW
EXECUTE FUNCTION modify_trigger_function();

-- Trigger for INSERT operations
CREATE TRIGGER insert_trigger
BEFORE INSERT ON my_table
FOR EACH ROW
EXECUTE FUNCTION modify_trigger_function();

-- Step 1: Create the users
CREATE USER api_one WITH PASSWORD 'password_one';
CREATE USER api_two WITH PASSWORD 'password_two';

-- Step 2: Grant permissions to the users
GRANT SELECT, INSERT, UPDATE, DELETE ON my_table TO api_one;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_table TO api_two;