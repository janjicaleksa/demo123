from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from typing import List, Optional
from pathlib import Path
import os

from ..core.config import get_settings

settings = get_settings()

class AzureBlobService:
    def __init__(self):
        self.connection_string = settings.azure_storage_connection_string
        self.container_name = settings.blob_container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self._ensure_container_exists()

    def _ensure_container_exists(self):
        try:
            self.blob_service_client.create_container(self.container_name)
        except ResourceExistsError:
            pass

    def _get_container_client(self) -> ContainerClient:
        return self.blob_service_client.get_container_client(self.container_name)

    async def upload_file(self, client_name: str, file_path: str, file_content: bytes) -> str:
        """Upload a file to Azure Blob Storage under the client's folder."""
        blob_path = f"{client_name}/{Path(file_path).name}"
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_path
        )
        
        await blob_client.upload_blob(file_content, overwrite=True)
        return blob_client.url

    async def delete_client_files(self, client_name: str):
        """Delete all files for a specific client."""
        container_client = self._get_container_client()
        blobs = container_client.list_blobs(name_starts_with=f"{client_name}/")
        
        for blob in blobs:
            try:
                container_client.delete_blob(blob.name)
            except ResourceNotFoundError:
                pass

    async def get_client_files(self, client_name: str) -> List[str]:
        """Get all file URLs for a specific client."""
        container_client = self._get_container_client()
        blobs = container_client.list_blobs(name_starts_with=f"{client_name}/")
        
        urls = []
        for blob in blobs:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob.name
            )
            urls.append(blob_client.url)
        
        return urls

    def is_valid_extension(self, filename: str) -> bool:
        """Check if the file extension is allowed."""
        return Path(filename).suffix.lower() in settings.allowed_extensions 