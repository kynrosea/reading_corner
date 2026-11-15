import datetime
import sqlite3

def adapt_date_iso(val: datetime.date) -> str:
    return val.isoformat()

sqlite3.register_adapter(datetime.date, adapt_date_iso)

def convert_date(val: bytes) -> datetime.date:
    return datetime.date.fromisoformat(val.decode())

sqlite3.register_converter('date', convert_date)
