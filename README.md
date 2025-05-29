# Factify Document Intelligence System

This project is a solution for the GenAI Engineer Candidate Task from Factify.  
It transforms static business documents into structured, AI-ready JSON representations, enabling seamless integration with downstream APIs and intelligent workflows.

---

## How to Run

### 1. Install Dependencies

Make sure you have **Python 3.10+** installed.  
It's recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

### 2. Set Your OpenAI API Key

You can either:

- Add a `.env` file:

```env
OPENAI_API_KEY=your_key_here
```

- Or set an environment variable manually:

**Windows CMD**
```cmd
set OPENAI_API_KEY=your_key_here
```

**Mac/Linux**
```bash
export OPENAI_API_KEY=your_key_here
```

### 3. Place Your Input PDFs

Put your files into the following directory:

```
data/input_pdfs/
```

### 4. Run Document Processing Pipeline

```bash
python main.py
```

This will:

- Load and parse PDFs
- Classify document types using GPT-4o
- Extract structured metadata
- Save results to:

```
results/output_json/
```

### 5. Launch the API Server

```bash
uvicorn api.api_main:app --reload
```

---

## API Overview (Part 2)

### `POST /documents/analyze`

- Input: `filename` (string query param)
- Returns:
  - Document ID
  - Classification type & confidence
  - Raw text
  - Extracted metadata

---

### `GET /documents/{id}`

- Returns the full structured representation of a document (by UUID)
- Designed to be machine-consumable
- All fields follow a consistent, semantic schema

---

### `GET /documents/{id}/actions`

- Returns a list of suggested actions based on document type and content
- Filters:
  - `status`
  - `deadline`
  - `priority`

---

## Example Output

Each output is saved as a `.json` file under `results/output_json/` with the following structure:

```json
{
  "document_id": "uuid",
  "filename": "contract.PDF",
  "raw_text": "...",
  "classification": {
    "type": "Contract",
    "confidence": 0.998
  },
  "metadata": {
    "parties": [...],
    "effective_date": "...",
    "termination_date": "...",
    "key_terms": [...]
  }
}
```

---

## Project Structure

```
api/
├── api_main.py             # Entry point for API server (FastAPI)
├── endpoints.py            # API endpoint logic
└── schema.py               # Pydantic models and request/response schemas

classify/
└── classifier.py           # LLM-based document type classification

data/
└── input_pdfs/             # Folder to store input PDF files

evaluation/
└── evaluate.py             # Evaluation or scoring logic (optional or for future use)
└── validate_metadata.py    # Prints null feilds

extract/
└── metadata_extractor.py   # Prompt-based metadata extraction from documents

models/
├── openai_client.py        # Wrapper for OpenAI API calls
└── prompts.py              # Prompt templates used in extraction/classification

results/
└── output_json/            # Folder for storing final structured JSON outputs

utils/
└── config.py               # Configuration and path management

main.py                     # Main processing script
README.md                   # Project documentation
requirements.txt            # Python dependencies

```

---

## Part 1: LLM-Based Document Intelligence

- Uses **GPT-4o** with zero-shot prompts for classification
- Prompt-based extraction tailored to each document type
- Confidence scores via token-level logprobs
- Missing fields handled gracefully (`null`)
- Output schema designed for API and AI usage
- Simple evaluation techniques were added. 

  ### Evaluation Summary
    - Classification: Confusion matrix and F1-score measured for the 3-label classifier.
    - Metadata Extraction: Missing fields are automatically logged per document, based on its type-specific schema.

        Note: For consistency, all metadata fields are included in the JSON output, even if they are irrelevant for a given document type.
---

## Part 2: AI-Ready API

- FastAPI-based mock server with 3 clean endpoints
- Each response includes field-level structure, type safety, and fallback handling
- Swagger UI available at `/docs`
- Consistent schemas with Pydantic models

---
## Part 3: Design Rationale and Production Considerations

### 1. Design Decisions

- **Zero-shot classification using GPT-4o**  
  Enables fast, cost-effective, and flexible document categorization for three predefined types without fine-tuning or labeled training data.

- **Prompt-based metadata extraction**  
  Each document type uses a dedicated and type-aware prompt template, ensuring accurate field extraction that aligns with business requirements.

- **Modular architecture**  
  The codebase is split by responsibility (e.g., `classify/`, `extract/`, `api/`, `utils/`), making it easy to test, debug, or extend individual components.

- **Consistent and flexible schema**  
  All documents include the full set of metadata fields in the JSON output — even if not applicable to the current document type — to provide a unified interface for downstream systems.

- **Graceful handling of missing fields**  
  Instead of hallucinating values or failing, the system returns `null` or predefined fallbacks such as `"TBD"` where relevant.

---

### 2. AI-Powered Feature Suggestions

#### Feature 1: Smart Date-Based Reminders

- **What it does**: Automatically detects fields like `due_date`, `termination_date`, or `reporting_period`, and generates time-based reminders.

- **How it works**:  
  The system produces a list of `actions` for each document, enriched with `status`, `priority`, and optional `deadline` fields — making it compatible with business tools like task managers or alert systems.

- **Business value**:  
  Helps prevent missed deadlines, improves compliance, and supports lightweight automation of document tracking.

#### Feature 2: Intelligent Document Workflow Agent

- **What it does**:  
  An AI agent (external to the current system) uses the extracted metadata to route and manage documents in real time. It can:
  - Route documents to the correct department or user (e.g., contracts to finance, reports to executives)
  - Identify which documents are most urgent based on `type`, `priority`, or `deadline`
  - Flag missing critical fields and suggest human review

- **How it works**:  
  The agent interacts with the system's API, analyzes metadata like `key_terms`, `document_type`, and deadlines, and triggers automated workflows or escalations as needed.

- **Business value**:  
  This transforms static documents into active workflow items. Instead of a passive API, the organization gains a real-time, AI-enhanced decision system — a document task manager that improves response time and prioritization.

---

### 3. Production Considerations

- **LLM API Failures**
  - All GPT-based operations are wrapped in `try/except` blocks
  - If an error occurs, the system responds with HTTP `503` and an informative error message
  - Logs are recorded for future debugging
  - Implement exponential backoff with jitter to handle rate limits or network spikes gracefully

- **Caching Strategy**
  - Each document is stored using a unique `document_id` (UUID).
  - To avoid reprocessing, the system checks if the document already exists in the output folder.
  - Optional: compute a hash of the raw text to detect if the PDF content has changed.

- **Cost Estimation**
  - **Classification step** (≈250 tokens): ~$0.002
  - **Metadata extraction** (≈1000 tokens): ~$0.01
  - **Total cost per document**: ~$0.012 using GPT-4o
  - **Additional costs** (cloud hosting, latency, compute): minimal when using FastAPI and OpenAI in a development-stage MVP
