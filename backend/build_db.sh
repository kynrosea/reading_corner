#!/bin/bash

DB="reading_tracker.db"

echo "Recreating database..."

rm -f "$DB"

sqlite3 "$DB" < "schema.sql"
sqlite3 "$DB" < "insert_data.sql"

echo
echo "Done :)"