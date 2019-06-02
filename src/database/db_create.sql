CREATE DATABASE case_db;

\c case_db

CREATE SCHEMA prod;

SET search_path TO prod;

CREATE TABLE prod.test_table (
   username VARCHAR (50) UNIQUE NOT NULL,
   email VARCHAR (155) UNIQUE NOT NULL
);

INSERT INTO PROD.test_table (username, email) 
VALUES ('uname', 'uname@domain.com');
