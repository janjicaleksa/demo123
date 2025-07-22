# AI File processing

An AI-powered application for processing customer and supplier ledger cards using Azure services.

## Features

- Multi-format file upload support (.pdf, .docx, .xlsx)
- Automated table extraction using Azure Document Intelligence
- AI-powered unified table generation
- Client-based file organization
- Secure file storage using Azure Blob Storage
- Export results in JSON or XLSX format

## Prerequisites

- Python 3.8+
- Azure subscription with:
  - Azure Blob Storage
  - Azure Document Intelligence
  - Azure AI Foundry

## Environment Setup

1. Create a `.env` file in the project root with the following variables:

```env
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your_endpoint
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_key
AZURE_AI_FOUNDRY_ENDPOINT=your_endpoint
AZURE_AI_FOUNDRY_KEY=your_key
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /upload/` - Upload files with client name
- `POST /extract/` - Extract tables from documents
- `POST /generate-report/` - Generate unified table
- `GET /results/{client}` - Fetch results for a client

## Project Structure

```
/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   │   └── config.py
│   ├── services/
│   │   ├── azure_blob.py
│   │   ├── document_intelligence.py
│   │   └── ai_processor.py
│   └── models/
│       └── schemas.py
├── static/
├── templates/
├── .env
├── main.py
└── requirements.txt
```

## License

MIT 
