-- USER
CREATE TABLE IF NOT EXISTS users (
    id CHAR(26) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS users_email_idx ON users (email);

-- CITY
CREATE TABLE IF NOT EXISTS cities (
    id CHAR(26) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS cities_name_idx ON cities (name);

-- WEATHER
CREATE TABLE IF NOT EXISTS weather_records (
    id CHAR(26) PRIMARY KEY,
    city_name VARCHAR(255) NOT NULL,

    day DATE NOT NULL,
    description VARCHAR(255) NOT NULL,
    temp DECIMAL(5,2) NOT NULL,
    temp_min DECIMAL(5,2) NOT NULL,
    temp_max DECIMAL(5,2) NOT NULL,
    feels_like DECIMAL(5,2) NOT NULL,
    humidity INT NOT NULL,
    wind_speed DECIMAL(5,2) NOT NULL,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL,

    CONSTRAINT fk_weathers_city FOREIGN KEY (city_name) REFERENCES cities(name) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS weather_city_name_idx ON weather_records (city_name);
CREATE INDEX IF NOT EXISTS weather_day_idx ON weather_records (day);
