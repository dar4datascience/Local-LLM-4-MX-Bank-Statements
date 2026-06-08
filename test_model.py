#!/usr/bin/env python3
"""Quick test of qwen2.5:3b with Spanish bank statement extraction."""
import ollama
import json

test_text = """
BBVA Bancomer
Estado de Cuenta - Tarjeta de Crédito
Periodo: Enero 2024

Movimientos:
15/01/2024  OXXO COMPRA CENTRO           $125.50 MXN
16/01/2024  UBER TRIP CDMX               $89.00 MXN
18/01/2024  LIVERPOOL COMPRA             $1,250.00 MXN
20/01/2024  PAGO RECIBIDO                $2,000.00 MXN
"""

prompt = f"""Extract ALL transactions from this bank statement. Return ONLY a JSON array.

Each transaction must have:
- date (YYYY-MM-DD format)
- description (merchant name)
- amount (number only, no symbols)
- currency (MXN)

Example format:
[
  {{"date": "2024-01-15", "description": "OXXO COMPRA", "amount": 125.50, "currency": "MXN"}}
]

Bank Statement:
{test_text}

JSON array:"""

print("Testing qwen2.5:3b with Spanish bank statement...\n")
print("=" * 60)

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": prompt}],
    format="json"
)

result = response['message']['content']
print(result)
print("=" * 60)

try:
    parsed = json.loads(result)
    print(f"\n✓ Valid JSON with {len(parsed)} transactions")
    for txn in parsed:
        print(f"  {txn.get('date')} | {txn.get('description')} | ${txn.get('amount')} {txn.get('currency')}")
except json.JSONDecodeError as e:
    print(f"\n✗ JSON parse error: {e}")
