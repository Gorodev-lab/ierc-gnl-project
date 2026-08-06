import re, zlib
from pathlib import Path
import pandas as pd

def extract_zip_stream(zip_path, year, target_dir):
    '''Extract ZIP and process each CSV to H3 Parquet.'''
    with open(zip_path, 'rb') as f:
        data = f.read()
    
    pk_positions = [m.start() for m in re.finditer(b'PK\x03\x04', data)]
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    
    all_dfs = []
    for i, pos in enumerate(pk_positions):
        fn_len = int.from_bytes(data[pos+26:pos+28], 'little')
        extra_len = int.from_bytes(data[pos+28:pos+30], 'little')
        compressed_size = int.from_bytes(data[pos+18:pos+22], 'little')
        uncompressed_size = int.from_bytes(data[pos+22:pos+26], 'little')
        try:
            filename = data[pos+30:pos+30+fn_len].decode('utf-8')
        except UnicodeDecodeError:
            filename = data[pos+30:pos+30+fn_len].decode('latin-1')
        
        compressed_start = pos + 30 + fn_len + extra_len
        compressed_data = data[compressed_start:compressed_start+compressed_size]
        
        try:
            decompressed = zlib.decompress(compressed_data, -zlib.MAX_WBITS)
        except zlib.error:
            try:
                decompressed = zlib.decompress(compressed_data)
            except zlib.error:
                print(f'  SKIP {filename}: decompression failed')
                continue
        
        # Parse CSV directly from bytes
        import io
        df = pd.read_csv(io.BytesIO(decompressed))
        
        # Filter to Gulf bbox
        if 'cell_ll_lat' in df.columns and 'cell_ll_lon' in df.columns:
            df = df[
                (df['cell_ll_lat'] >= 22.5) & (df['cell_ll_lat'] <= 32.0) &
                (df['cell_ll_lon'] >= -115.0) & (df['cell_ll_lon'] <= -108.0)
            ]
            if len(df) > 0:
                df['year'] = year
                all_dfs.append(df)
                print(f'  {filename}: {len(df)} Gulf rows')
        
        if i % 20 == 0:
            print(f'  Processed {i+1}/{len(pk_positions)} files')
    
    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        print(f'Total Gulf rows for {year}: {len(combined)}')
        return combined
    return pd.DataFrame()

# Process 2016
print("=== Processing 2016 ===")
df_2016 = extract_zip_stream(
    '/home/gorops/ierc-gnl-project/data/raw/gfw/fleet-daily-csvs-100-v3-2016.zip',
    2016,
    '/home/gorops/ierc-gnl-project/lakehouse/processed/gfw/fishing_effort_h3/year=2016'
)

# Process 2020  
print("\n=== Processing 2020 ===")
df_2020 = extract_zip_stream(
    '/home/gorops/ierc-gnl-project/data/raw/gfw/zenodo_global_fishing_watch_fleet-daily-csvs-100-v3-2020.zip',
    2020,
    '/home/gorops/ierc-gnl-project/lakehouse/processed/gfw/fishing_effort_h3/year=2020'
)

# Combine and save
if not df_2016.empty and not df_2020.empty:
    combined = pd.concat([df_2016, df_2020], ignore_index=True)
elif not df_2016.empty:
    combined = df_2016
else:
    combined = df_2020

if not combined.empty:
    print(f'\n=== Combined: {len(combined)} rows ===')
    print(f'Columns: {list(combined.columns)}')
    print(combined.head().to_string())
    
    # Add H3 column
    import sys
    sys.path.insert(0, '/home/gorops/ierc-gnl-project/src')
    from src.utils.h3 import add_h3_column_vectorized
    combined = add_h3_column_vectorized(combined, 'cell_ll_lat', 'cell_ll_lon', 'h3_cell', 8)
    
    # Add time partition
    combined['date'] = pd.to_datetime(combined['date'])
    combined['month'] = combined['date'].dt.month
    combined['time_partition'] = combined['date'].dt.strftime('%Y-%m')
    
    # Save partitioned parquet
    output_base = Path('/home/gorops/ierc-gnl-project/lakehouse/processed/gfw/fishing_effort_h3')
    for (year, month), group in combined.groupby(['year', 'month']):
        out_dir = output_base / f'year={year}' / f'month={month:02d}'
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / 'part-0.parquet'
        group.to_parquet(out_file, compression='zstd')
        print(f'  Saved {len(group)} rows to {out_file}')
    
    # Also save combined for GeoJSON export
    combined.to_parquet('/home/gorops/ierc-gnl-project/data/processed/gfw_gulf_combined.parquet', compression='zstd')
    print(f'\nSaved combined to gfw_gulf_combined.parquet ({len(combined)} rows)')