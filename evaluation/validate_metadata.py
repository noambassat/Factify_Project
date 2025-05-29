# evaluation/validate_metadata.py

from pathlib import Path
import json

# Define relevant fields for each document type
REQUIRED_FIELDS = {
    "Invoice": ["vendor", "amount", "due_date", "line_items"],
    "Contract": ["parties", "effective_date", "termination_date", "key_terms"],
    "Earnings": ["reporting_period", "key_metrics", "executive_summary"]
}

def validate_metadata_structure(output_dir="results/output_json"):
    base_path = Path(output_dir)
    all_files = list(base_path.glob("*.json"))
    for file in all_files:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)

        doc_type = data.get("classification", {}).get("type", "Unknown")
        metadata = data.get("metadata", {})
        missing = []

        for key in REQUIRED_FIELDS.get(doc_type, []):
            if metadata.get(key) in [None, "", [], {}]:
                missing.append(key)

        print(f"\n{file.name} [{doc_type}]")
        if missing:
            print("Missing required fields:", ", ".join(missing))
        else:
            print("All required fields are present.")

        print("-" * 40)
