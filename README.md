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
-Zero-shot classification using GPT-4o
  Enables fast, low-cost, and flexible classification for three document types without fine-tuning or training.
-Prompt-based metadata extraction
  Each document type uses a dedicated template to extract precise fields as defined in the task.
-Modular architecture
  The codebase is clearly separated by responsibility: classification, extraction, API, and evaluation.
-Consistent and flexible schema
  All metadata fields are present in every JSON, even if they are not applicable to the current document type — ensuring compatibility with downstream systems.
-Graceful handling of missing fields
  Instead of failing or hallucinating, the system returns null or a well-structured fallback such as "TBD".

### 2. AI-Powered Feature Suggestions
#### - Feature 1: Smart Date-Based Reminders
    What it does:
    Automatically detects fields like due_date, termination_date, or reporting_period, and generates time-based reminders.
    
    How it works:
    Each document generates a list of structured actions with status, priority, and optional deadlines — designed for task management tools or alerts.
    
    Business value:
    Reduces risk of missed deadlines, supports operational automation, and enables intelligent monitoring of business obligations.

#### - Feature 2: Intelligent Document Workflow Agent
    What it does:
    An AI agent operates above the API layer and receives structured metadata. It makes contextual decisions such as:
    
    Who should receive this document?
    
    Is any important field missing and needs human attention?
    
    Which document is most urgent?
    
    How it works:
    The agent analyzes fields like type, priority, deadline, and key_terms, and routes the document or alerts relevant stakeholders in real-time.
    
    Business value:
    Transforms static documents into autonomous, actionable items. Replaces manual sorting with a smart document task manager — enabling AI-powered workflows.

### 3. Production Considerations
 - LLM API Failures
  All LLM calls are wrapped in try/except.
  In case of failure, the system returns HTTP 503 with a clear error message.
  Errors are logged for debugging and tracing purposes.
  
  Suggested improvement: implement exponential backoff with jitter to handle rate limits or network spikes gracefully.

-Caching Strategy
  Each document is stored by its document_id.
  
  Optional: generate a hash fingerprint of the PDF to detect changes and avoid redundant processing.

- Cost Estimation
  Classification (short text, ~250 tokens): ~$0.002
  
  Metadata extraction (~1000 tokens): ~$0.01
  
  Total per document: ~$0.012 using GPT-4o
  
  Additional costs (infrastructure, latency, cloud storage) are minimal for an MVP using FastAPI and OpenAI.
  





