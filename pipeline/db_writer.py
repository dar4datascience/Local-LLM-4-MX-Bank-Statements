import duckdb
from pathlib import Path
from .schema import Transaction


def get_db_path() -> Path:
    """Get path to DuckDB file."""
    return Path(__file__).parent.parent / "db" / "transactions.duckdb"


def init_db():
    """Create transactions table if not exists."""
    db_path = get_db_path()
    
    with duckdb.connect(str(db_path)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                date DATE NOT NULL,
                description VARCHAR NOT NULL,
                amount DOUBLE NOT NULL,
                currency VARCHAR NOT NULL,
                type VARCHAR NOT NULL,
                card_name VARCHAR NOT NULL,
                source_file VARCHAR NOT NULL,
                PRIMARY KEY (date, description, amount, card_name, source_file)
            )
        """)
        print(f"✓ Database initialized at {db_path}")


def upsert_transactions(transactions: list[Transaction]):
    """Insert or replace transactions in DuckDB."""
    if not transactions:
        return
    
    db_path = get_db_path()
    
    with duckdb.connect(str(db_path)) as conn:
        for txn in transactions:
            conn.execute("""
                INSERT OR REPLACE INTO transactions 
                (date, description, amount, currency, type, card_name, source_file)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                txn.date,
                txn.description,
                txn.amount,
                txn.currency,
                txn.type.value,
                txn.card_name,
                txn.source_file
            ])
        
        print(f"✓ Upserted {len(transactions)} transactions")


def get_transaction_count() -> int:
    """Get total transaction count."""
    db_path = get_db_path()
    
    with duckdb.connect(str(db_path)) as conn:
        result = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()
        return result[0] if result else 0
