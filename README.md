# MX Bank Statements — Local LLM Parser

Parse Mexican bank statements (PDF) using local Ollama LLM, store transactions in DuckDB, and visualize in a Shiny dashboard.

## Features

- **PDF Extraction**: Handles both text-based and image-based PDFs (OCR via Tesseract)
- **LLM-Powered Parsing**: Ollama extracts structured transaction data from unstructured statements
- **DuckDB Storage**: Fast, embedded database for all transactions
- **Shiny Dashboard**: Interactive tables (Great Tables) + AI chat assistant

## Supported Banks

- BBVA (Nómina, Crédito)
- HSBC Crédito
- RAPPI
- PLATAka
- INVEX
- STORI
- NU

## Setup

### Prerequisites

1. **Python 3.11+** (managed via `uv`)
2. **Ollama** installed and running ([ollama.ai](https://ollama.ai))
3. **Tesseract OCR** for image-based PDFs:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr tesseract-ocr-spa
   
   # macOS
   brew install tesseract tesseract-lang
   ```

### Installation

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <repo-url>
cd Local-LLM-4-MX-Bank-Statements

# Install dependencies
uv sync

# Pull recommended Ollama model
ollama pull llama3.2
```

## Usage

### 1. Add Bank Statements

Drop PDF files into `data/statements/`:

```bash
cp ~/Downloads/bbva_*.pdf data/statements/
```

### 2. Run Extraction Pipeline

```bash
uv run python -m pipeline.run
```

This will:
- Extract text from PDFs (OCR if needed)
- Call Ollama to parse transactions
- Write to `db/transactions.duckdb`

### 3. Launch Dashboard

```bash
uv run shiny run --port 8086 app/app.py
```

Open [http://localhost:8086](http://localhost:8086)

**Tabs:**
- **Credit Cards**: All credit card transactions
- **Debit Cards**: All debit/checking account transactions  
- **Chat Assistant**: Ask questions about your spending (powered by Ollama)

## Development

### Run Tests

```bash
uv run pytest
```

### Playwright E2E Tests

```bash
# Install Playwright browsers
uv run playwright install

# Run dashboard tests
uv run pytest tests/test_dashboard.py
```

## Architecture

```
pipeline/          # Data extraction
  ├── pdf_loader   # pdfplumber + OCR fallback
  ├── llm_extractor # Ollama structured output
  └── db_writer    # DuckDB upsert

app/               # Shiny dashboard
  ├── modules/
  │   ├── transactions_table  # Great Tables display
  │   └── chat_assistant      # Ollama chat interface
  └── app.py       # Main Shiny app
```

## Ollama Models

Recommended: `llama3.2` (default) or `mistral`

For better accuracy with Spanish text:
```bash
ollama pull mistral
```

Then update `pipeline/llm_extractor.py` to use `model="mistral"`.