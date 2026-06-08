from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict


class TransactionType(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class Transaction(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2024-01-15",
                "description": "OXXO COMPRA",
                "amount": 125.50,
                "currency": "MXN",
                "type": "debit",
                "card_name": "BBVA Nomina",
                "source_file": "bbva_nomina_2024_01.pdf"
            }
        }
    )
    
    date: date
    description: str
    amount: float
    currency: str = "MXN"
    type: TransactionType
    card_name: str
    source_file: str
