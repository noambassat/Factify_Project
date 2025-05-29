# main.py
from config import PDF_INPUT_FOLDER, OUTPUT_FOLDER
from utils.pdf_loader import load_documents
from classify.classifier import classify_document
from extract.metadata_extractor import extract_metadata
from evaluation.evaluate import evaluate_predictions
import json
import os

def save_json(doc, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    base_filename, _ = os.path.splitext(doc.filename)
    json_filename = base_filename + ".json"
    path = os.path.join(output_dir, json_filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(doc.to_api_dict(), indent=2, ensure_ascii=False))

def main():
    docs = load_documents(PDF_INPUT_FOLDER)
    for doc in docs:
        classify_document(doc)
        extract_metadata(doc)
        save_json(doc, OUTPUT_FOLDER)

    evaluate_predictions(docs)


if __name__ == "__main__":
    main()
