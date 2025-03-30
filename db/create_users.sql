-- Step 1: Create the users
CREATE USER api_one WITH PASSWORD 'password_one';
CREATE USER api_two WITH PASSWORD 'password_two';

-- Step 2: Grant permissions to the users
GRANT SELECT, INSERT, UPDATE, DELETE ON my_table TO api_one;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_table TO api_two;