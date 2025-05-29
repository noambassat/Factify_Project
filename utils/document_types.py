# utils/document_types.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import uuid
import json

@dataclass
class Document:
    document_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    filename: str = ""
    raw_text: str = ""
    chunks: List[str] = field(default_factory=list)
    metadata: Dict[str, Optional[str]] = field(default_factory=dict)
    true_label: str = ""
    predicted_label: str = ""
    label_confidence: Dict[str, float] = field(default_factory=dict)

    def to_json(self):
        return json.dumps(self.__dict__, indent=2, ensure_ascii=False)

    def to_api_dict(self):
        return {
            "document_id": self.document_id,
            "filename": self.filename,
            "raw_text": self.raw_text,
            "classification": {
                "type": self.predicted_label,
                "confidence": self.label_confidence.get(self.predicted_label, 0.0)
            },
            "metadata": self.metadata
        }
