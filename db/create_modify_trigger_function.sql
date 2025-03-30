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