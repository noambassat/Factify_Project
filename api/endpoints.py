# api/endpoints.py

import os
import json
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from api.schema import DocumentResponse, ActionList, ActionItem, ClassificationResult, DocumentMetadata

router = APIRouter()
OUTPUT_DIR = "results/output_json"

def load_document_by_id(document_id: str) -> DocumentResponse:
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(OUTPUT_DIR, filename), encoding="utf-8") as f:
                data = json.load(f)
                if data.get("document_id") == document_id:
                    return DocumentResponse(
                        document_id=data["document_id"],
                        filename=data["filename"],
                        raw_text=data["raw_text"],
                        classification=ClassificationResult(
                            type=data["classification"]["type"],
                            confidence=data["classification"]["confidence"]
                        ),
                        metadata=DocumentMetadata(**data.get("metadata", {}))
                    )
    raise HTTPException(status_code=404, detail="Document not found")


@router.post("/documents/analyze", response_model=DocumentResponse)
def analyze_document(filename: str):
    json_filename = os.path.splitext(filename)[0].lower() + ".json"

    for fname in os.listdir(OUTPUT_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(OUTPUT_DIR, fname), encoding="utf-8") as f:
                data = json.load(f)
                if data["filename"].lower() == filename.lower():

                    return DocumentResponse(
                        document_id=data["document_id"],
                        filename=data["filename"],
                        raw_text=data.get("raw_text", ""),
                        classification=ClassificationResult(
                            type=data["classification"]["type"],
                            confidence=data["classification"]["confidence"]
                        ),
                        metadata=DocumentMetadata(**data.get("metadata", {}))
                    )
    raise HTTPException(status_code=404, detail="File not found")


@router.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str):
    """
    Returns all metadata for a specific document.
    Includes structured fields and classification info.
    """
    return load_document_by_id(document_id)


@router.get("/documents/{document_id}/actions", response_model=ActionList)
def get_document_actions(
    document_id: str,
    status: Optional[str] = Query(None),
    deadline: Optional[str] = Query(None),
    priority: Optional[str] = Query(None)
):
    """
    Returns a list of suggested actions for a given document.
    Supports filtering by status, deadline or priority.
    """
    doc = load_document_by_id(document_id)
    actions = []

    if doc.classification.type == "Invoice" and doc.metadata.due_date:
        actions.append(ActionItem(
            type="payment",
            description="Schedule payment for invoice",
            deadline=doc.metadata.due_date,
            priority="high"
        ))

    if doc.classification.type == "Contract" and doc.metadata.termination_date:
        actions.append(ActionItem(
            type="review",
            description="Prepare for contract termination",
            deadline=doc.metadata.termination_date,
            priority="medium"
        ))

    if doc.classification.type == "Earnings" and doc.metadata.key_metrics:
        actions.append(ActionItem(
            type="report",
            description="Review financial performance summary",
            priority="low"
        ))

    # Apply filtering
    if status:
        actions = [a for a in actions if a.status == status]
    if deadline:
        actions = [a for a in actions if a.deadline == deadline]
    if priority:
        actions = [a for a in actions if a.priority == priority]

    return ActionList(document_id=document_id, actions=actions)
