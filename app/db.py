import duckdb
import pandas as pd
from pathlib import Path


def get_db_path() -> Path:
    """Get path to DuckDB file."""
    return Path(__file__).parent.parent / "db" / "transactions.duckdb"


def get_transactions(card_type: str = None) -> pd.DataFrame:
    """
    Get transactions from DuckDB, optionally filtered by card type.
    
    Args:
        card_type: "credit" or "debit" to filter, None for all
    
    Returns:
        DataFrame with transactions
    """
    db_path = get_db_path()
    
    if not db_path.exists():
        return pd.DataFrame(columns=[
            "date", "description", "amount", "currency", 
            "type", "card_name", "source_file"
        ])
    
    with duckdb.connect(str(db_path), read_only=True) as conn:
        if card_type:
            query = """
                SELECT date, description, amount, currency, type, card_name, source_file
                FROM transactions
                WHERE type = ?
                ORDER BY date DESC
            """
            df = conn.execute(query, [card_type]).df()
        else:
            query = """
                SELECT date, description, amount, currency, type, card_name, source_file
                FROM transactions
                ORDER BY date DESC
            """
            df = conn.execute(query).df()
    
    return df


def get_db_schema() -> str:
    """Get database schema for LLM context."""
    return """
Database: transactions.duckdb
Table: transactions
Columns:
  - date (DATE): Transaction date
  - description (VARCHAR): Merchant or transaction description
  - amount (DOUBLE): Transaction amount in local currency
  - currency (VARCHAR): Currency code (usually MXN)
  - type (VARCHAR): "credit" or "debit"
  - card_name (VARCHAR): Bank/card name (BBVA Nomina, HSBC Credito, etc.)
  - source_file (VARCHAR): Original PDF filename

Example queries:
  - Total spending: SELECT SUM(amount) FROM transactions WHERE type = 'credit'
  - By card: SELECT card_name, SUM(amount) FROM transactions GROUP BY card_name
  - Recent: SELECT * FROM transactions ORDER BY date DESC LIMIT 10
"""
