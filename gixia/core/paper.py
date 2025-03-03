from datetime import datetime
from dataclasses import dataclass, fields


@dataclass
class Paper:
    id: str
    title: str
    authors: list[str]
    abstract: str
    updated: datetime
    arxiv_metadata: dict = None
    arxiv_raw_metadata: dict = None

    @classmethod
    def from_document(cls, document: dict):
        """
        Convert a MongoDB document to a Paper object.
        """
        # Keep only data fields
        field_names = [field.name for field in fields(cls)]
        document = {k: v for k, v in document.items() if k in field_names}
        return cls(**document)