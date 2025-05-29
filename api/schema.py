from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union

class ClassificationResult(BaseModel):
    type: str = Field(..., description="The predicted type of the document (e.g., Invoice, Contract, Earnings)")
    confidence: float = Field(..., description="The confidence score of the classification result")

class LineItem(BaseModel):
    description: str = Field(..., description="Description of the line item")
    amount: str = Field(..., description="Amount of the line item")

class DocumentMetadata(BaseModel):
    vendor: Optional[str] = Field(None, description="Vendor name in an invoice document")
    amount: Optional[str] = Field(None, description="Total amount in an invoice")
    due_date: Optional[str] = Field(None, description="Due date for payment if applicable")
    line_items: Optional[List[LineItem]] = Field(None, description="List of line items in the invoice")

    parties: Optional[List[str]] = Field(None, description="Parties involved in the contract")
    effective_date: Optional[str] = Field(None, description="Start date of the contract")
    termination_date: Optional[str] = Field(None, description="End or termination date of the contract")
    key_terms: Optional[List[str]] = Field(None, description="Important contractual terms")

    reporting_period: Optional[str] = Field(None, description="Reporting period in earnings report")
    key_metrics: Optional[Dict[str, Union[str, float]]] = Field(None, description="Key financial metrics from the report")
    executive_summary: Optional[str] = Field(None, description="Executive summary of the earnings report")

class DocumentResponse(BaseModel):
    document_id: str = Field(..., description="Unique identifier for the document")
    filename: str = Field(..., description="Original filename of the document")
    raw_text: Optional[str] = Field(None, description="Full extracted raw text from the document")
    classification: ClassificationResult = Field(..., description="Classification result and confidence")
    metadata: DocumentMetadata = Field(..., description="Extracted metadata based on document type")

class ActionItem(BaseModel):
    type: str = Field(..., description="Type of action to take")
    description: str = Field(..., description="What the user should do")
    priority: Optional[str] = Field("medium", description="Priority of the action")
    status: Optional[str] = Field("pending", description="Current status of the action")
    deadline: Optional[str] = Field(None, description="Deadline for taking this action if applicable")

class ActionList(BaseModel):
    document_id: str = Field(..., description="Document ID the actions relate to")
    actions: List[ActionItem] = Field(..., description="List of suggested actions")
