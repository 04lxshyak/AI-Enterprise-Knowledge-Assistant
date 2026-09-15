"""
Utilities for file handling with Supabase Storage.
"""
from fastapi import UploadFile
from typing import List, Optional, Dict
from supabase import create_client, Client
from app.core.environment import settings
import uuid
from pathlib import Path


class SupabaseStorage:
    """Handles files in Supabase Storage."""
    
    def __init__(self, supabase_url: str, supabase_key: str, bucket_name: str):
        self.client: Client = create_client(supabase_url, supabase_key)
        self.bucket_name = bucket_name
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self) -> None:
        """Checks that the bucket exists and logs a warning if it does not."""
        try:
            buckets = self.client.storage.list_buckets()
            bucket_exists = any(b.name == self.bucket_name for b in buckets)
            if not bucket_exists:
                print(f"Warning: Bucket '{self.bucket_name}' does not exist in Supabase")
        except Exception as e:
            print(f"Warning: Could not verify bucket existence: {e}")
    
    async def save_uploaded_file(self, file: UploadFile, filename: Optional[str] = None, user_id: Optional[int] = None) -> str:
        """
        Saves a file in Supabase Storage.
        If user_id is provided, saves it under user_<user_id>/filename.
        Returns: The file path in Supabase (path/to/file.ext).
        """
        base_filename = filename or file.filename or f"uploaded_{uuid.uuid4()}"
        
        # Organize by user when user_id is provided.
        if user_id:
            dest_name = f"user_{user_id}/{base_filename}"
        else:
            dest_name = base_filename
        
        # Read the file content.
        file_content = await file.read()
        
        # Upload to Supabase Storage.
        try:
            response = self.client.storage.from_(self.bucket_name).upload(
                path=dest_name,
                file=file_content,
                file_options={"content-type": file.content_type or "application/octet-stream"}
            )
            
            # Return the file path in Supabase.
            return dest_name
        except Exception as e:
            # If the file already exists, try to update it.
            if "duplicate" in str(e).lower() or "already exists" in str(e).lower():
                self.client.storage.from_(self.bucket_name).update(
                    path=dest_name,
                    file=file_content,
                    file_options={"content-type": file.content_type or "application/octet-stream"}
                )
                return dest_name
            raise Exception(f"Error uploading file to Supabase: {e}")
    
    async def save_uploaded_files(self, files: List[UploadFile], user_id: Optional[int] = None) -> List[str]:
        """Saves multiple files in Supabase Storage."""
        saved_paths = []
        
        for file in files:
            path = await self.save_uploaded_file(file, user_id=user_id)
            saved_paths.append(path)
        
        return saved_paths
    
    def delete_file(self, file_path: str) -> bool:
        """Deletes a file from Supabase Storage."""
        try:
            self.client.storage.from_(self.bucket_name).remove([file_path])
            return True
        except Exception as e:
            print(f"Warning: Could not delete file {file_path}: {e}")
            return False
    
    def file_exists(self, file_path: str) -> bool:
        """Checks whether a file exists in Supabase Storage."""
        try:
            files = self.client.storage.from_(self.bucket_name).list()
            return any(f['name'] == file_path for f in files)
        except Exception as e:
            print(f"Warning: Could not check file existence: {e}")
            return False
    
    def get_file_info(self, file_path: str) -> Dict:
        """
        Gets file information from Supabase Storage.
        Returns: Dict with filename, file_type, file_size_bytes, file_path, and public_url.
        """
        try:
            # Get the public URL for the file.
            public_url = self.get_public_url(file_path)
            
            # Extract path information.
            path_obj = Path(file_path)
            filename = path_obj.name
            file_type = path_obj.suffix.lower().replace(".", "")
            
            # Try to get file metadata.
            try:
                # If the path has folders (for example, user_1/file.pdf), list inside that folder.
                path_parts = file_path.split('/')
                if len(path_parts) > 1:
                    folder = '/'.join(path_parts[:-1])  # user_1
                    files = self.client.storage.from_(self.bucket_name).list(folder)
                    matching_file = next((f for f in files if f['name'] == filename), None)
                else:
                    files = self.client.storage.from_(self.bucket_name).list()
                    matching_file = next((f for f in files if f['name'] == file_path), None)
                
                file_size = matching_file.get('metadata', {}).get('size', 0) if matching_file else 0
            except Exception as e:
                print(f"Warning: Could not get file size for {file_path}: {e}")
                file_size = 0
            
            return {
                "filename": filename,
                "file_type": file_type,
                "file_size_bytes": file_size,
                "file_path": file_path,
                "public_url": public_url
            }
        except Exception as e:
            print(f"Warning: Could not get file info for {file_path}: {e}")
            return {}
    
    def get_public_url(self, file_path: str) -> str:
        """Gets the public URL for a file."""
        try:
            response = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
            return response
        except Exception as e:
            print(f"Warning: Could not get public URL: {e}")
            return ""
    
    def get_signed_url(self, file_path: str, expires_in: int = 3600) -> str:
        """
        Gets a temporary signed URL for private access.
        expires_in: expiration time in seconds (default: 1 hour).
        """
        try:
            response = self.client.storage.from_(self.bucket_name).create_signed_url(
                path=file_path,
                expires_in=expires_in
            )
            return response.get('signedURL', '')
        except Exception as e:
            print(f"Warning: Could not create signed URL: {e}")
            return ""
    
    def download_file(self, file_path: str) -> bytes:
        """Downloads a file from Supabase Storage."""
        try:
            response = self.client.storage.from_(self.bucket_name).download(file_path)
            return response
        except Exception as e:
            raise Exception(f"Error downloading file from Supabase: {e}")


# Global reusable instance.
storage = SupabaseStorage(
    supabase_url=settings.SUPABASE_URL,
    supabase_key=settings.SUPABASE_KEY,
    bucket_name=settings.SUPABASE_BUCKET
)
