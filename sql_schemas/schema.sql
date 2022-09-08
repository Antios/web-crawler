CREATE DATABASE IF NOT EXISTS url_database;

USE url_database;

CREATE TABLE IF NOT EXISTS links(
    link VARCHAR(255) PRIMARY KEY,
    link_timestamp TIMESTAMP NOT NULL DEFAULT current_timestamp ON UPDATE current_timestamp
)