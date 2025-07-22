from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
import json

from ...services.azure_blob import AzureBlobService
from ...services.document_intelligence import DocumentIntelligenceService
from ...services.ai_processor import AIProcessor
from ...models.schemas import (
    UploadResponse,
    ExtractionResponse,
    UnifiedReport,
    ErrorResponse
)

router = APIRouter()
blob_service = AzureBlobService()
doc_service = DocumentIntelligenceService()
ai_processor = AIProcessor()

@router.post("/upload/", response_model=UploadResponse)
async def upload_files(
    client_name: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """Upload files for a client."""
    try:
        # Validate file extensions
        for file in files:
            if not blob_service.is_valid_extension(file.filename):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid file type: {file.filename}"
                )

        # Delete existing files for the client
        await blob_service.delete_client_files(client_name)

        # Upload new files
        uploaded_files = []
        for file in files:
            content = await file.read()
            file_url = await blob_service.upload_file(
                client_name,
                file.filename,
                content
            )
            uploaded_files.append(file_url)

        return UploadResponse(
            client_name=client_name,
            uploaded_files=uploaded_files,
            upload_time=datetime.now(),
            status="success"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/extract/", response_model=ExtractionResponse)
async def extract_tables(client_name: str):
    """Extract tables from uploaded files."""
    try:
        # Get all files for the client
        file_urls = await blob_service.get_client_files(client_name)
        if not file_urls:
            raise HTTPException(
                status_code=404,
                detail=f"No files found for client: {client_name}"
            )

        # Extract tables from each file
        all_tables = []
        for file_url in file_urls:
            tables = await doc_service.extract_tables(file_url)
            all_tables.extend(tables)

        return ExtractionResponse(
            client_name=client_name,
            extracted_tables=all_tables,
            status="success"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/generate-report/", response_model=UnifiedReport)
async def generate_report(client_name: str):
    """Generate unified report from extracted tables."""
    try:
        # First extract tables
        extraction_response = await extract_tables(client_name)
        
        # Generate unified report
        report = await ai_processor.generate_unified_report(
            client_name,
            extraction_response.extracted_tables
        )
        
        return report

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/results/{client_name}")
async def get_results(client_name: str):
    """Get the latest results for a client."""
    try:
        # Generate a new report
        report = await generate_report(client_name)
        
        # Convert to dict for JSON response
        return JSONResponse(
            content=json.loads(report.json())
        )

    except Exception as e:
        return ErrorResponse(
            detail=str(e)
        ) 