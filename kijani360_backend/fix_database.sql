-- Fix missing columns in KijaniCare360 database

-- Add missing columns to tree_planting_streaks table
ALTER TABLE tree_planting_streaks 
ADD COLUMN IF NOT EXISTS last_activity_date TIMESTAMP;

-- Add missing columns to users table if they don't exist
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS total_points INTEGER DEFAULT 0;

-- Add missing columns to other streak tables
ALTER TABLE watering_streaks 
ADD COLUMN IF NOT EXISTS last_activity_date TIMESTAMP;

-- Update existing records to have default values
UPDATE tree_planting_streaks 
SET last_activity_date = created_at 
WHERE last_activity_date IS NULL;

UPDATE watering_streaks 
SET last_activity_date = created_at 
WHERE last_activity_date IS NULL;

-- Show table structure to verify
\d tree_planting_streaks;
\d users;