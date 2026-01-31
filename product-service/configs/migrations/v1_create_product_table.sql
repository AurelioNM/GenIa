CREATE TABLE IF NOT EXISTS products (
    id CHAR(26) PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL,
    description TEXT NULL,
    price NUMERIC(10, 2) NOT NULL,
    category VARCHAR(200) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS products_name_idx ON products (name);
CREATE INDEX IF NOT EXISTS products_category_idx ON products (category);
CREATE INDEX IF NOT EXISTS products_active_idx ON products (active);
