import json
import ollama
from pathlib import Path
from .schema import Transaction, TransactionType


BANK_PROMPTS = {
    "hsbc_credito": {
        "keywords": ["HSBC"],
        "type": TransactionType.CREDIT,
        "card_name": "HSBC Credito"
    },
    "bbva_nomina": {
        "keywords": ["BBVA", "Nómina", "Cuenta de nómina"],
        "type": TransactionType.DEBIT,
        "card_name": "BBVA Nomina"
    },
    "bbva_credito": {
        "keywords": ["BBVA", "Crédito", "Tarjeta de crédito"],
        "type": TransactionType.CREDIT,
        "card_name": "BBVA Credito"
    },
    "rappi": {
        "keywords": ["Rappi", "RappiCard"],
        "type": TransactionType.CREDIT,
        "card_name": "RAPPI"
    },
    "plataka": {
        "keywords": ["Plataka", "PLATAka"],
        "type": TransactionType.DEBIT,
        "card_name": "PLATAka"
    },
    "invex": {
        "keywords": ["Invex", "INVEX"],
        "type": TransactionType.CREDIT,
        "card_name": "INVEX"
    },
    "stori": {
        "keywords": ["Stori", "STORI"],
        "type": TransactionType.CREDIT,
        "card_name": "STORI"
    },
    "nu": {
        "keywords": ["Nu", "NU", "Nubank"],
        "type": TransactionType.CREDIT,
        "card_name": "NU"
    }
}


def detect_bank(text: str, filename: str) -> dict:
    """
    Detect bank from text content or filename.
    """
    text_lower = text.lower()
    filename_lower = filename.lower()
    
    for bank_key, config in BANK_PROMPTS.items():
        for keyword in config["keywords"]:
            if keyword.lower() in text_lower or keyword.lower() in filename_lower:
                return config
    
    return {
        "type": TransactionType.DEBIT,
        "card_name": "Unknown"
    }


def build_extraction_prompt(text: str, bank_config: dict) -> str:
    """
    Build structured extraction prompt for Ollama.
    """
    return f"""You are a financial data extraction assistant. Extract ALL transactions from this bank statement.

Bank: {bank_config['card_name']}
Transaction Type: {bank_config['type'].value}

Extract each transaction with these fields:
- date (YYYY-MM-DD format)
- description (merchant/concept)
- amount (positive number, no currency symbols)
- currency (default MXN)

Return ONLY a valid JSON array of transactions. Example format:
[
  {{"date": "2024-01-15", "description": "OXXO COMPRA", "amount": 125.50, "currency": "MXN"}},
  {{"date": "2024-01-16", "description": "UBER TRIP", "amount": 89.00, "currency": "MXN"}}
]

Bank Statement Text:
{text[:8000]}

JSON array of transactions:"""


def extract_transactions(text: str, source_file: Path, model: str = "qwen2.5:3b") -> list[Transaction]:
    """
    Extract transactions using Ollama with structured output.
    """
    bank_config = detect_bank(text, source_file.name)
    prompt = build_extraction_prompt(text, bank_config)
    
    print(f"  → Detected bank: {bank_config['card_name']} ({bank_config['type'].value})")
    print(f"  → Calling Ollama model: {model}")
    
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            format="json"
        )
        
        raw_json = response['message']['content']
        transactions_data = json.loads(raw_json)
        
        if not isinstance(transactions_data, list):
            print(f"  → Warning: Expected list, got {type(transactions_data)}")
            return []
        
        transactions = []
        for item in transactions_data:
            try:
                transaction = Transaction(
                    date=item["date"],
                    description=item["description"],
                    amount=float(item["amount"]),
                    currency=item.get("currency", "MXN"),
                    type=bank_config["type"],
                    card_name=bank_config["card_name"],
                    source_file=source_file.name
                )
                transactions.append(transaction)
            except Exception as e:
                print(f"  → Skipping invalid transaction: {e}")
                continue
        
        print(f"  → Extracted {len(transactions)} transactions")
        return transactions
    
    except Exception as e:
        print(f"  → Extraction failed: {e}")
        return []
