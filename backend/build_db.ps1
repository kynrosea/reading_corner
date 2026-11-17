# Force PowerShell's stream encoding to UTF-8
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 > $null

$DB = "backend/reading_tracker.db"

Write-Output "Recreating fresh database..."

if (Test-Path $DB -PathType Leaf) {
    Remove-Item $DB
}

sqlite3 $DB ".read backend/app/sql/schema.sql"
sqlite3 $DB ".read backend/app/sql/insert_data.sql"

Write-Output ""
Write-Output "Done :)"
