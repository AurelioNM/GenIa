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

ALTER TABLE weather_records ADD CONSTRAINT uq_weather_city_day UNIQUE (city_name, day);
CREATE INDEX IF NOT EXISTS weather_city_name_idx ON weather_records (city_name);
CREATE INDEX IF NOT EXISTS weather_day_idx ON weather_records (day);
