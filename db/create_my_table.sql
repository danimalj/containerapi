CREATE TABLE my_table (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    text_field TEXT,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL, -- Updated default value
    updated_by TEXT
) TABLESPACE other;