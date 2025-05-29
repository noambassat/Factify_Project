# api/schema.py
from typing import List, Optional, Dict, Union
from pydantic import BaseModel

class ClassificationResult(BaseModel):
    type: str
    confidence: float

class LineItem(BaseModel):
    description: str
    amount: str

class DocumentMetadata(BaseModel):
    vendor: Optional[str] = None
    amount: Optional[str] = None
    due_date: Optional[str] = None
    line_items: Optional[List[LineItem]] = None

    parties: Optional[List[str]] = None
    effective_date: Optional[str] = None
    termination_date: Optional[str] = None
    key_terms: Optional[List[str]] = None

    reporting_period: Optional[str] = None
    key_metrics: Optional[Dict[str, Union[str, float]]] = None
    executive_summary: Optional[str] = None

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    raw_text: Optional[str] = None
    classification: ClassificationResult
    metadata: DocumentMetadata

class ActionItem(BaseModel):
    type: str
    description: str
    priority: Optional[str] = "medium"
    status: Optional[str] = "pending"
    deadline: Optional[str] = None

class ActionList(BaseModel):
    document_id: str
    actions: List[ActionItem]
