CREATE TABLE IF NOT EXISTS users (
    id CHAR(26) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS users_email_idx ON users (email);

-- Populate
INSERT INTO users (id, email, password, created_at, updated_at)
VALUES
('01J8FQ6Z5X1A4MZ2E7K9Q0P1A1', 'alice@example.com', '$2b$10$hashedpassword1', NOW(), NULL),
('01J8FQ6Z6A8B9C2D3E4F5G6H7J', 'bob@example.com', '$2b$10$hashedpassword2', NOW(), NULL);
