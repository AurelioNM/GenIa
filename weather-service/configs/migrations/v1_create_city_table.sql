CREATE TABLE IF NOT EXISTS cities (
    id CHAR(26) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS cities_name_idx ON cities (name);
