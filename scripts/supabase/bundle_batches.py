#!/usr/bin/env python3
import os
import glob

SQL_DIR = "scripts/supabase/data_sql"
BUNDLE_DIR = "scripts/supabase/bundled_sql"
os.makedirs(BUNDLE_DIR, exist_ok=True)

def bundle(pattern, output_filename):
    files = sorted(glob.glob(os.path.join(SQL_DIR, pattern)))
    out_path = os.path.join(BUNDLE_DIR, output_filename)
    total_bytes = 0
    with open(out_path, "w", encoding="utf-8") as outfile:
        for f in files:
            with open(f, "r", encoding="utf-8") as infile:
                content = infile.read()
                outfile.write(content + "\n")
                total_bytes += len(content)
    print(f"Bundled {len(files)} files into {output_filename} ({total_bytes} bytes / {total_bytes/1024/1024:.2f} MB)")

if __name__ == "__main__":
    bundle("grilla_h3_*.sql", "01_grilla_h3_all.sql")
    bundle("features_summary_*.sql", "02_features_summary_all.sql")
    bundle("riqueza_*.sql", "03_riqueza_all.sql")
    print("Bundling complete!")
