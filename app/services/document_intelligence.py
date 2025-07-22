from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from typing import List, Dict, Any
import pandas as pd
import io

from ..core.config import get_settings
from ..models.schemas import TableData

settings = get_settings()

class DocumentIntelligenceService:
    def __init__(self):
        self.endpoint = settings.document_intelligence_endpoint
        self.key = settings.document_intelligence_key
        self.client = DocumentAnalysisClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )

    async def extract_tables(self, file_url: str) -> List[TableData]:
        """Extract tables from a document using Azure Document Intelligence."""
        try:
            poller = self.client.begin_analyze_document_from_url(
                "prebuilt-document",
                file_url
            )
            result = poller.result()
            
            extracted_tables = []
            fiscal_year = self._detect_fiscal_year(result)
            
            for table in result.tables:
                table_data = self._process_table(table)
                if table_data:
                    extracted_tables.append(
                        TableData(
                            fiscal_year=fiscal_year,
                            data=table_data
                        )
                    )
            
            return extracted_tables
        
        except Exception as e:
            raise Exception(f"Failed to extract tables: {str(e)}")

    def _detect_fiscal_year(self, result: Any) -> str:
        """Detect fiscal year from document content."""
        # Look for patterns like "Accounting period 01.01.2023 – 31.12.2023"
        content = " ".join([p.content for p in result.paragraphs])
        
        # Add your fiscal year detection logic here
        # This is a placeholder implementation
        import re
        year_pattern = r"20\d{2}"
        years = re.findall(year_pattern, content)
        
        if years:
            return years[0]
        return "Unknown"

    def _process_table(self, table: Any) -> List[Dict]:
        """Convert table to structured data."""
        rows = []
        headers = []
        
        # Extract headers from the first row
        for cell in table.cells:
            if cell.row_index == 0:
                headers.append(cell.content)
        
        # Process data rows
        current_row = -1
        row_data = {}
        
        for cell in table.cells:
            if cell.row_index == 0:
                continue
                
            if cell.row_index != current_row:
                if row_data:
                    rows.append(row_data)
                current_row = cell.row_index
                row_data = {}
            
            header = headers[cell.column_index] if cell.column_index < len(headers) else f"Column{cell.column_index}"
            row_data[header] = cell.content
        
        if row_data:
            rows.append(row_data)
        
        return rows 