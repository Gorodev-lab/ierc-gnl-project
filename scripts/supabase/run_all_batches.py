#!/usr/bin/env python3
import os
import glob
import json
import urllib.request
import urllib.parse

# Read publishable key or anon key
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpoZ2R3aG9iZWZveW9kcnNtcG5jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU5NjI5NTgsImV4cCI6MjEwMTUzODk1OH0.Ii8gWRA1xDEFzZqZGkWsaTlulug0Tp1z4JAPGIrIMEY"
SUPABASE_URL = "https://jhgdwhobefoyodrsmpnc.supabase.co"

SQL_DIR = "scripts/supabase/data_sql"

def get_sql_files():
    pattern = os.path.join(SQL_DIR, "*.sql")
    return sorted(glob.glob(pattern))

if __name__ == "__main__":
    files = get_sql_files()
    print(f"Found {len(files)} SQL batch files in {SQL_DIR}.")
    for f in files:
        size = os.path.getsize(f)
        print(f"  {os.path.basename(f)} ({size} bytes)")
