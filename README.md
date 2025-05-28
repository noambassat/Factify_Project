# Factify Document Intelligence System

This project is a solution for the GenAI Engineer Candidate Task from Factify.  
It processes business documents (invoices, contracts, and earnings reports), classifies them using LLMs, and extracts structured metadata.

## How to Run

1. Install dependencies  
   Make sure you have Python 3.10+ installed.  
   It is recommended to use a virtual environment.

   pip install -r requirements.txt

2. Set your OpenAI API key  
   You can either:
   - Add a .env file with the line:
     OPENAI_API_KEY=your_key_here
   - Or set an environment variable:

     For Windows CMD:
     set OPENAI_API_KEY=your_key_here

     For Mac/Linux:
     export OPENAI_API_KEY=your_key_here

3. Place your input PDF documents in:

   data/input_pdfs/

4. Run the pipeline:

   python main.py

5. Results  
   Output files will be saved in:

   results/output_json/

## Classification and Metadata Extraction

- Zero-shot classification using OpenAI's GPT-4o
- Supported types: Invoice, Contract, Earnings
- Confidence scores are included
- Structured metadata is extracted based on document type
- Robust handling of missing or partial fields

## Output JSON Format

Each processed document is saved as a JSON with the following structure:

{
  "document_id": "generated_uuid",
  "filename": "invoice1.pdf",
  "true_label": "Invoice",
  "predicted_label": "Invoice",
  "label_confidence": {
    "Invoice": 0.98
  },
  "metadata": {
    "vendor": "Example LLC",
    "amount": "$1299.00",
    "due_date": "2024-03-25",
    "line_items": [
      {
        "description": "Consulting Services",
        "amount": "$1000.00"
      },
      {
        "description": "VAT",
        "amount": "$299.00"
      }
    ]
  }
}

## Project Structure

- main.py — Entry point for document processing
- config.py — Configuration constants and folder paths
- models/openai_client.py — OpenAI client setup
- models/prompts.py — Prompt templates for each document type
- classify/classifier.py — LLM-based document classification
- extract/metadata_extractor.py — Metadata extraction based on predicted type
- utils/pdf_loader.py — PDF parsing and raw text extraction
- results/output_json/ — Output folder for generated JSONs

## Part 1 — Completed

- LLM classification of document types
- Prompt-based structured metadata extraction
- Output includes confidence levels
- Graceful degradation for missing fields
- Works on unseen documents in production structure

## Part 2 and 3

A REST-style mock API and written design document are provided separately in api_docs.md.
