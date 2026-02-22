CREATE TABLE IF NOT EXISTS users (
    id CHAR(26) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS users_email_idx ON users (email);
