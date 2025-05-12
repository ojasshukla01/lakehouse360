import os
import json
import pandas as pd
import duckdb
from pathlib import Path

INPUT_FOLDER = Path("data/json_files")
OUTPUT_FOLDER = Path("validation/profiles")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

def profile_table(file_path: Path, table_name: str):
    try:
        # Load the JSON file into a Pandas DataFrame
        df = pd.read_json(file_path, orient='records', lines=False)
        if df.empty:
            raise ValueError("Empty dataframe.")

        # Connect to DuckDB in-memory DB
        con = duckdb.connect(database=':memory:')
        con.register(table_name, df)

        # Get column-wise statistics
        profile_query = f"""
        SELECT 
            column_name,
            MIN(value) AS min_value,
            MAX(value) AS max_value,
            COUNT(*) AS total_count,
            COUNT(*) - COUNT(value) AS null_count,
            COUNT(DISTINCT value) AS distinct_count
        FROM (
            SELECT 
                column_name,
                UNNEST([%s]) AS value
            FROM (
                SELECT 
                    UNNEST(['%s']) AS column_name
            )
        ) 
        GROUP BY column_name;
        """ % (
            ', '.join([f'"{col}"' for col in df.columns]),
            "', '".join(df.columns)
        )

        # Alternatively, collect stats per column via Python for simplicity
        profile = []
        for col in df.columns:
            series = df[col]
            profile.append({
                "column": col,
                "dtype": str(series.dtype),
                "min": str(series.min()) if pd.api.types.is_numeric_dtype(series) else None,
                "max": str(series.max()) if pd.api.types.is_numeric_dtype(series) else None,
                "null_count": int(series.isnull().sum()),
                "distinct_count": int(series.nunique())
            })

        # Save profile to JSON
        output_path = OUTPUT_FOLDER / f"{table_name}_profile.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2)

        print(f"✅ Profiled {file_path.name}")
    except Exception as e:
        print(f"⚠️ Failed to profile {file_path.name}: {e}")

def main():
    files = list(INPUT_FOLDER.glob("*.json"))
    if not files:
        print("❌ No JSON files found to profile.")
        return

    for file_path in files:
        table_name = file_path.stem
        profile_table(file_path, table_name)

if __name__ == "__main__":
    main()
