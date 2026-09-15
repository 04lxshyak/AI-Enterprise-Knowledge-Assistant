from sqlalchemy.orm import Session
from app.modules.documents.models import Document
from typing import List, Optional
from pathlib import Path


class DocumentRepository:
    """Repository for document database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_document(
        self,
        filename: str,
        file_path: Optional[str],
        file_type: str,
        chunks_count: int = 0,
        file_size_bytes: Optional[int] = None,
        user_id: Optional[int] = None,
        status: str = "processed"
    ) -> Document:
        """Creates a new document in the database."""
        document = Document(
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            chunks_count=chunks_count,
            file_size_bytes=file_size_bytes,
            user_id=user_id,
            status=status
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_document_by_filename(self, filename: str) -> Optional[Document]:
        """Returns a document by filename."""
        return self.db.query(Document).filter(Document.filename == filename).first()
    
    def generate_unique_filename(self, filename: str) -> str:
        """Generates a unique filename if one already exists."""
        path = Path(filename)
        stem = path.stem  # Name without extension.
        suffix = path.suffix  # .pdf, .docx, etc.
        
        # Check whether the original name already exists.
        if not self.get_document_by_filename(filename):
            return filename
        
        # Find a unique name by incrementing the counter.
        counter = 1
        while True:
            new_filename = f"{stem}_{counter}{suffix}"
            if not self.get_document_by_filename(new_filename):
                return new_filename
            counter += 1

    def get_document_by_filename_and_user(self, filename: str, user_id: int) -> Optional[Document]:
        """Returns a document by filename and user."""
        return self.db.query(Document).filter(
            Document.filename == filename,
            Document.user_id == user_id
        ).first()

    def get_document_by_id(self, document_id: int) -> Optional[Document]:
        """Returns a document by ID."""
        return self.db.query(Document).filter(Document.id == document_id).first()

    def get_all_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """Returns all documents with pagination."""
        return self.db.query(Document).order_by(Document.upload_date.desc()).offset(skip).limit(limit).all()

    def get_documents_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Document]:
        """Returns documents for a specific user with pagination."""
        return self.db.query(Document).filter(
            Document.user_id == user_id
        ).order_by(Document.upload_date.desc()).offset(skip).limit(limit).all()

    def count_documents(self) -> int:
        """Counts all documents."""
        return self.db.query(Document).count()

    def count_documents_by_user(self, user_id: int) -> int:
        """Counts documents for a specific user."""
        return self.db.query(Document).filter(Document.user_id == user_id).count()

    def delete_document(self, document_id: int) -> bool:
        """Deletes a document and its associated embeddings through cascade."""
        document = self.get_document_by_id(document_id)
        if document:
            self.db.delete(document)
            self.db.commit()
            return True
        return False

    def update_document_processing_result(self, document_id: int, chunks_count: int, status: str, indexing_cost: float | None = None) -> bool:
        """Updates the full processing result."""
        document = self.get_document_by_id(document_id)
        if document:
            document.chunks_count = chunks_count
            document.status = status
            if indexing_cost is not None:
                document.indexing_cost = indexing_cost
            self.db.commit()
            self.db.refresh(document)
            return True
        return False

    def update_document_status(self, document_id: int, status: str) -> bool:
        """Updates only the document status."""
        document = self.get_document_by_id(document_id)
        if document:
            document.status = status
            self.db.commit()
            self.db.refresh(document)
            return True
        return False

    def update_document_metadata(self, document_id: int, **kwargs) -> bool:
        """Updates document metadata."""
        document = self.get_document_by_id(document_id)
        if document:
            for key, value in kwargs.items():
                if hasattr(document, key):
                    setattr(document, key, value)
            self.db.commit()
            self.db.refresh(document)
            return True
        return False

