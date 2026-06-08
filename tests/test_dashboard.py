import pytest
from playwright.sync_api import Page, expect
import subprocess
import time
import signal
import os


@pytest.fixture(scope="module")
def shiny_server():
    """Start Shiny server for testing."""
    process = subprocess.Popen(
        ["uv", "run", "shiny", "run", "--port", "8086", "app/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    time.sleep(5)
    
    yield "http://localhost:8086"
    
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait()


def test_dashboard_loads(page: Page, shiny_server):
    """Test that dashboard loads successfully."""
    page.goto(shiny_server)
    
    expect(page).to_have_title("MX Bank Statements Dashboard")
    
    page.screenshot(path="test-results/dashboard-home.png")


def test_credit_tab_renders(page: Page, shiny_server):
    """Test Credit Cards tab renders."""
    page.goto(shiny_server)
    
    credit_tab = page.get_by_role("tab", name="Credit Cards")
    credit_tab.click()
    
    expect(page.locator("text=Credit Transactions")).to_be_visible()
    
    page.screenshot(path="test-results/credit-tab.png")


def test_debit_tab_renders(page: Page, shiny_server):
    """Test Debit Cards tab renders."""
    page.goto(shiny_server)
    
    debit_tab = page.get_by_role("tab", name="Debit Cards")
    debit_tab.click()
    
    expect(page.locator("text=Debit Transactions")).to_be_visible()
    
    page.screenshot(path="test-results/debit-tab.png")


def test_chat_assistant_ui_loads(page: Page, shiny_server):
    """Test Chat Assistant tab loads."""
    page.goto(shiny_server)
    
    chat_tab = page.get_by_role("tab", name="Chat Assistant")
    chat_tab.click()
    
    expect(page.locator("text=Ask about your spending")).to_be_visible()
    
    page.screenshot(path="test-results/chat-tab.png")


def test_tables_present_or_empty_message(page: Page, shiny_server):
    """Test that either Great Tables render or empty state message shows."""
    page.goto(shiny_server)
    
    credit_tab = page.get_by_role("tab", name="Credit Cards")
    credit_tab.click()
    
    has_table = page.locator("table").count() > 0
    has_empty_msg = page.locator("text=No credit transactions found").count() > 0
    
    assert has_table or has_empty_msg, "Should show either table or empty message"
