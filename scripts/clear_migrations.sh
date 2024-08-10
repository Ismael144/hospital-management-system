#!/usr/bin/bash

# Define the path to your Django project
project_path="C:/Users/swale/Desktop/hms"

# Get all migration folders within the project
migration_folders=$(find "$project_path" -type d -name "migrations")

# Database path
sqlite_db="db.sqlite3"

# Iterate over each migration folder
for folder in $migration_folders; do
    # Get all Python files in the migration folder except __init__.py
    migration_files=$(find "$folder" -type f -name "*.py" ! -name "__init__.py")
    # Delete each migration file
    for file in $migration_files; do
        rm -f "$file"
        echo "Deleted: $file"
    done

    # Checking whether sqlite3 db exists
    if [ -f "$sqlite_db" ]; then
        rm -f "$sqlite_db"
        echo "Deleted: $sqlite_db"
    fi
done

echo "All migrations cleared!"