import pytest
from pathlib import Path
from pipeline.llm_extractor import detect_bank, build_extraction_prompt
from pipeline.schema import TransactionType


def test_detect_bank_bbva_nomina():
    """Test bank detection for BBVA Nomina."""
    text = "BBVA Bancomer\nCuenta de Nómina\nMovimientos del periodo"
    config = detect_bank(text, "bbva_nomina_2024.pdf")
    
    assert config["card_name"] == "BBVA Nomina"
    assert config["type"] == TransactionType.DEBIT


def test_detect_bank_hsbc_credito():
    """Test bank detection for HSBC Credito."""
    text = "HSBC\nEstado de Cuenta Tarjeta de Crédito"
    config = detect_bank(text, "hsbc_statement.pdf")
    
    assert config["card_name"] == "HSBC Credito"
    assert config["type"] == TransactionType.CREDIT


def test_detect_bank_from_filename():
    """Test bank detection from filename when text doesn't match."""
    text = "Generic bank statement"
    config = detect_bank(text, "rappi_card_2024.pdf")
    
    assert config["card_name"] == "RAPPI"
    assert config["type"] == TransactionType.CREDIT


def test_detect_bank_unknown():
    """Test fallback for unknown bank."""
    text = "Unknown Bank Statement"
    config = detect_bank(text, "unknown.pdf")
    
    assert config["card_name"] == "Unknown"
    assert config["type"] == TransactionType.DEBIT


def test_build_extraction_prompt():
    """Test prompt building."""
    text = "Sample transaction text"
    config = {
        "card_name": "BBVA Nomina",
        "type": TransactionType.DEBIT
    }
    
    prompt = build_extraction_prompt(text, config)
    
    assert "BBVA Nomina" in prompt
    assert "debit" in prompt
    assert "JSON array" in prompt
    assert "Sample transaction text" in prompt
