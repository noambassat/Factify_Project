
# Factify Document Intelligence System

This project is a solution for the GenAI Engineer Candidate Task from Factify.  
It processes business documents (invoices, contracts, and earnings reports), classifies them using LLMs, and extracts structured metadata into a well-defined, API-ready format.

---

## 🛠️ How to Run

### 1. Install Dependencies

Make sure you have **Python 3.10+** installed.  
It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

### 2. Set Your OpenAI API Key

You can either:

- Add a `.env` file with the following line:

```
OPENAI_API_KEY=your_key_here
```

- Or set an environment variable manually:

**Windows CMD:**
```cmd
set OPENAI_API_KEY=your_key_here
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY=your_key_here
```

### 3. Place Your Input PDF Documents

Save your PDF files under:

```
data/input_pdfs/
```

### 4. Run the Processing Pipeline

```bash
python main.py
```

This will:

- Extract the text
- Classify the document type
- Extract semantic metadata
- Save results to:

```
results/output_json/
```

### 5. Start the Mock API Server

```bash
uvicorn api.api_main:app --reload
```

---

## 🔗 API Endpoints (Part 2)

### `POST /documents/analyze`

- Accepts the filename of a previously processed document.
- Returns:
  - Full metadata
  - Classification type and confidence
  - Raw text

### `GET /documents/{id}`

- Returns all structured information for the given document ID.
- Designed to be easily consumable by AI agents.

### `GET /documents/{id}/actions`

- Returns a list of suggested actions based on the document type and metadata.
- Supports optional filtering by:
  - `status`
  - `deadline`
  - `priority`

---

## 📄 Output JSON Format

Each processed document is saved in `results/output_json/` with the following structure:

```json
{
  "document_id": "generated_uuid",
  "filename": "invoice1.pdf",
  "raw_text": "...",
  "classification": {
    "type": "Invoice",
    "confidence": 0.97
  },
  "metadata": {
    "vendor": "Example LLC",
    "amount": "$1299.00",
    "due_date": "2024-03-25",
    "line_items": [
      { "description": "Consulting Services", "amount": "$1000.00" },
      { "description": "VAT", "amount": "$299.00" }
    ]
  }
}
```

---

## 📁 Project Structure

```
main.py                       # Entry point for processing documents
config.py                     # Paths and environment configuration

models/
│   └── openai_client.py      # OpenAI API client wrapper
│   └── prompts.py            # Prompt templates for metadata extraction

classify/classifier.py        # LLM-based document type classification
extract/metadata_extractor.py # Prompt-based metadata extraction

utils/
│   └── pdf_loader.py         # PDF parsing utilities
│   └── document_types.py     # Document object structure

api/                          # FastAPI endpoints and schema

data/input_pdfs/              # Place PDF files here
results/output_json/          # Output folder for JSON results
```

---

## 🧠 Part 1 — Summary

- **Zero-shot classification** using GPT-4o  
- **Prompt-based structured extraction** per document type  
- Supports 3 types: `Invoice`, `Contract`, `Earnings`  
- Handles missing fields gracefully (returns `null`)  
- Saves structured outputs consumable by AI systems  

---

## 🌐 Part 2 — REST API Summary

- Exposes classification & metadata via clean API  
- Includes semantic actions per document type  
- Designed for composability: descriptive fields & consistent format  
- Supports filtering for downstream consumption  

---

## 💬 Part 3 — Talking Points

### 1. Design Decisions

- **Zero-shot Classification**: Chosen for simplicity and speed. With only 3 document types, it performs well.
- **Prompt-based Extraction**: Specific prompts per document type to extract fields into structured JSON.
- **Modular Design**: Components are cleanly separated for clarity and testability.
- **Graceful Fallbacks**: Missing metadata returns `null` instead of breaking.

### 2. AI-Powered Features for Factify

#### Feature 1: Document Timeline Alerts

- **Use case**: Trigger reminders from fields like `due_date` or `termination_date`.
- **Implementation**: API returns suggested actions with time-sensitive recommendations.
- **Value**: Proactively supports business deadlines and compliance.

#### Feature 2: Semantic Document Comparison

- **Use case**: Compare two versions of a contract or report.
- **Implementation**: Embed both versions and highlight semantic differences.
- **Value**: Enables smart, AI-powered review workflows for legal/HR/finance.

### 3. Production Considerations

- **LLM API Failures**:
  - Handled with `try/except`
  - Fallback to cached results if available
  - Return HTTP 503 with descriptive message if necessary

- **Caching Strategy**:
  - Save processed documents by UUID and filename
  - Reuse on repeated analysis to save cost

- **Cost Estimation**:
  - ~2 GPT-4o calls per document (~500 tokens per call)
  - Estimated cost: ~$0.01 per document

---
