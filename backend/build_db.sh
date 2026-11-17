#!/bin/bash

DB="backend/reading_tracker.db"

echo "Recreating fresh database..."

rm -f "$DB"

sqlite3 "$DB" < "backend/app/sql/schema.sql"
sqlite3 "$DB" < "backend/app/sql/insert_data.sql"

echo
echo "Done :)"
