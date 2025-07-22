from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class UploadResponse(BaseModel):
    client_name: str
    uploaded_files: List[str]
    upload_time: datetime
    status: str

class ExtractionRequest(BaseModel):
    client_name: str
    file_urls: List[str]

class TableData(BaseModel):
    fiscal_year: str
    data: List[Dict]

class ExtractionResponse(BaseModel):
    client_name: str
    extracted_tables: List[TableData]
    status: str

class ReportRequest(BaseModel):
    client_name: str
    extracted_tables: List[TableData]

class YearSummary(BaseModel):
    total_debit: float = Field(default=0.0)
    total_credit: float = Field(default=0.0)
    balance: float = Field(default=0.0)

class UnifiedReport(BaseModel):
    client_name: str
    previous_year: YearSummary
    current_year: YearSummary
    generation_time: datetime
    status: str

class ErrorResponse(BaseModel):
    detail: str
    status: str = "error" 