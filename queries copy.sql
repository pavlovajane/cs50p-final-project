-- SQL queries to create tables and input, read data

-- Create users and their passwords table
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" TEXT NOT NULL,
    "hash" TEXT NOT NULL);

-- Create data table for storing of the scrapped data
CREATE TABLE IF NOT EXISTS "scripts" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "movie" TEXT NOT NULL,
    "scene_number" INTEGER,
    "scene_name" TEXT,
    "type" TEXT CHECK("type" IN ('dialogue','direction') ),
    "character" TEXT,
    "text" TEXT NOT NULL);

-- User's top quotes
CREATE TABLE IF NOT EXISTS "tops" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INTEGER,
    "quote_id" INTEGER,
    FOREIGN KEY (quote_id) REFERENCES scripts (id)
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE INDEX quote_idx_name ON scripts(movie, scene_name);
CREATE INDEX quote_idx_number ON scripts(movie, scene_number);
CREATE INDEX scene_idx ON scripts(movie);