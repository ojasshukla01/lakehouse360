import os
import json
import pandas as pd
from pathlib import Path

INPUT_DIR = Path("data")
OUTPUT_DIR = INPUT_DIR / "json_files"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def convert_file_to_json(input_path: Path):
    ext = input_path.suffix.lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(input_path)
        elif ext == ".tsv":
            df = pd.read_csv(input_path, sep="\t")
        elif ext == ".parquet":
            df = pd.read_parquet(input_path)
        elif ext == ".jsonl":
            df = pd.read_json(input_path, lines=True)
        elif ext == ".json":
            print(f"⏩ Skipping already JSON: {input_path.name}")
            return
        else:
            print(f"❌ Unsupported file: {input_path.name}")
            return

        output_path = OUTPUT_DIR / f"{input_path.stem}.json"
        df.to_json(output_path, orient="records", indent=2)
        print(f"✅ Converted {input_path.name} -> {output_path.name}")
    except Exception as e:
        print(f"❌ Failed to convert {input_path.name}: {str(e)}")

if __name__ == "__main__":
    for file in INPUT_DIR.iterdir():
        if file.is_file():
            convert_file_to_json(file)
