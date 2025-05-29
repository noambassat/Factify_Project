# Factify API Documentation

This file describes the API endpoints used in the Factify document intelligence platform.

---

## POST /documents/analyze

**Description**:  
Accepts the filename of a document that has already been processed and returns its extracted metadata, raw text, and classification.

**Query Parameters**:  
- `filename` (string): The name of the processed file, e.g. `contract.PDF`

**Response Example**:
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
    "parties": ["Party A", "Party B"],
    "effective_date": "2023-01-01",
    "termination_date": "2024-01-01",
    "key_terms": ["Term A", "Term B"]
  }
}
```

---

## GET /documents/{id}

**Description**:  
Returns all metadata and classification information for the given document ID.

**Path Parameters**:  
- `id` (string): UUID of the document

**Response Example**:
```json
{
  "document_id": "uuid",
  "filename": "earnings.PDF",
  "raw_text": "...",
  "classification": {
    "type": "Earnings",
    "confidence": 0.991
  },
  "metadata": {
    "reporting_period": "Q1 2025",
    "key_metrics": {
      "Revenue": "90234",
      "Net Income": "34540"
    },
    "executive_summary": null
  }
}
```

---

## GET /documents/{id}/actions

**Description**:  
Returns a list of suggested actions for a given document based on its type and metadata.

**Path Parameters**:  
- `id` (string): UUID of the document

**Optional Query Parameters**:  
- `status` (string): Filter by action status (e.g. "pending")
- `deadline` (string): Filter by deadline date
- `priority` (string): Filter by action priority (e.g. "high")

**Response Example**:
```json
{
  "document_id": "uuid",
  "actions": [
    {
      "type": "review",
      "description": "Check contract for termination clauses",
      "priority": "medium",
      "status": "pending",
      "deadline": "TBD"
    }
  ]
}
```

---

## Notes

- All responses include consistent, semantic field names
- Missing fields are returned as `null`
- Designed to be AI-consumable and easy to integrate
