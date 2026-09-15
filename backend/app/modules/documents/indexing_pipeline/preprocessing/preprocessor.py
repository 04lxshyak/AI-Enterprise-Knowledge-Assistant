"""
Document preprocessor - technical layer
"""
from pathlib import Path
from typing import List, Dict
from .file_processors import process_docx, process_md, process_pdf


class Preprocessor:
    """Extracts and converts document content to the standard format."""
    
    SUPPORTED_EXTENSIONS = {
        ".pdf": process_pdf,
        ".docx": process_docx,
        ".md": process_md
    }
    
    def process_files(self, file_paths: List[Path], filename_mapping: Dict[str, str] = None) -> Dict[str, List]:
        """
        Processes a list of files and extracts their content.
        
        Args:
            file_paths: List of file paths.
            filename_mapping: Optional dictionary mapping file_path.name -> original_filename.
            
        Returns:
            Dict with filename as key and a list of Document objects as value.
        """
        results = {}
        filename_mapping = filename_mapping or {}
        
        for file_path in file_paths:
            if not file_path.exists() or not file_path.is_file():
                print(f"File does not exist or is not a file: {file_path}")
                continue
            
            filename = file_path.name
            ext = file_path.suffix.lower()
            original_filename = filename_mapping.get(filename)
            
            if ext in self.SUPPORTED_EXTENSIONS:
                processor_func = self.SUPPORTED_EXTENSIONS[ext]
                try:
                    documents = processor_func(file_path, original_filename)
                    results[filename] = documents
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    results[filename] = []
            else:
                print(f"Unsupported file type: {filename}")
                results[filename] = []
        
        return results
    
    def is_supported_file(self, file_path: Path) -> bool:
        """Checks whether the file type is supported."""
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS
