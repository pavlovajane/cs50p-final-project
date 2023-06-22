-- SQL queries to create tables and input, read data

-- Create data table for storing of the scrapped data
CREATE TABLE IF NOT EXISTS "scripts" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "movie" TEXT NOT NULL,
    "scene_number" INTEGER,
    "scene_name" TEXT,
    "character" TEXT,
    "type" TEXT CHECK("type" IN ('dialogue','direction') )
    "text" TEXT NOT NULL,
    crosstraining TEXT,
    marathontime REAL NOT NULL,
    performancecategory CHARACTER(1)
);