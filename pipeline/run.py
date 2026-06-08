#!/usr/bin/env python3
"""
Pipeline runner: scan PDFs, extract transactions, write to DuckDB.
"""
from pathlib import Path
from .pdf_loader import extract_text_from_pdf
from .llm_extractor import extract_transactions
from .db_writer import init_db, upsert_transactions, get_transaction_count


def main():
    print("=" * 60)
    print("MX Bank Statement Parser")
    print("=" * 60)
    
    init_db()
    
    statements_dir = Path(__file__).parent.parent / "data" / "statements"
    pdf_files = list(statements_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"\n⚠ No PDF files found in {statements_dir}")
        print("  Add your bank statements to data/statements/")
        return
    
    print(f"\n📄 Found {len(pdf_files)} PDF files\n")
    
    total_extracted = 0
    
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        
        text = extract_text_from_pdf(pdf_file)
        
        if not text.strip():
            print("  → No text extracted, skipping\n")
            continue
        
        transactions = extract_transactions(text, pdf_file)
        
        if transactions:
            upsert_transactions(transactions)
            total_extracted += len(transactions)
        
        print()
    
    final_count = get_transaction_count()
    
    print("=" * 60)
    print(f"✓ Pipeline complete")
    print(f"  Extracted: {total_extracted} transactions this run")
    print(f"  Total in DB: {final_count} transactions")
    print("=" * 60)


if __name__ == "__main__":
    main()
