from typing import List, Dict
from datetime import datetime
import pandas as pd

from ..models.schemas import TableData, UnifiedReport, YearSummary

class AIProcessor:
    def __init__(self):
        pass  # Add AI Foundry initialization here when available

    async def generate_unified_report(self, client_name: str, tables: List[TableData]) -> UnifiedReport:
        """Generate a unified report from extracted tables."""
        try:
            # Group tables by fiscal year
            tables_by_year = {}
            for table in tables:
                if table.fiscal_year not in tables_by_year:
                    tables_by_year[table.fiscal_year] = []
                tables_by_year[table.fiscal_year].extend(table.data)

            # Process each year's data
            years = sorted(tables_by_year.keys())
            if len(years) < 2:
                # If we only have one year, treat it as the current year
                current_year = years[0] if years else "Unknown"
                previous_year = "Unknown"
            else:
                current_year = years[-1]
                previous_year = years[-2]

            # Generate summaries
            previous_year_summary = self._generate_year_summary(
                tables_by_year.get(previous_year, [])
            )
            current_year_summary = self._generate_year_summary(
                tables_by_year.get(current_year, [])
            )

            return UnifiedReport(
                client_name=client_name,
                previous_year=previous_year_summary,
                current_year=current_year_summary,
                generation_time=datetime.now(),
                status="success"
            )

        except Exception as e:
            raise Exception(f"Failed to generate unified report: {str(e)}")

    def _generate_year_summary(self, data: List[Dict]) -> YearSummary:
        """Generate summary statistics for a year's data."""
        if not data:
            return YearSummary()

        try:
            # Convert string values to numeric
            df = pd.DataFrame(data)
            
            # Look for columns containing debit/credit information
            debit_cols = [col for col in df.columns if 'debit' in col.lower()]
            credit_cols = [col for col in df.columns if 'credit' in col.lower()]
            
            # Calculate totals
            total_debit = 0.0
            total_credit = 0.0
            
            for col in debit_cols:
                df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')
                total_debit += df[col].sum()
                
            for col in credit_cols:
                df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')
                total_credit += df[col].sum()
            
            return YearSummary(
                total_debit=total_debit,
                total_credit=total_credit,
                balance=total_debit - total_credit
            )
            
        except Exception:
            return YearSummary() 