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
