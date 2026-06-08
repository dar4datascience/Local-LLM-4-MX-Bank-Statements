from shiny import module, ui, render, reactive
from great_tables import GT
import pandas as pd
from ..db import get_transactions


@module.ui
def transactions_table_ui(card_type_label: str):
    """
    UI for transactions table module.
    
    Args:
        card_type_label: Display label (e.g., "Credit" or "Debit")
    """
    return ui.card(
        ui.card_header(f"{card_type_label} Transactions"),
        ui.output_ui("table_output"),
        ui.output_text_verbatim("summary")
    )


@module.server
def transactions_table_server(input, output, session, card_type: str):
    """
    Server logic for transactions table module.
    
    Args:
        card_type: "credit" or "debit"
    """
    
    @reactive.calc
    def data():
        return get_transactions(card_type)
    
    @render.ui
    def table_output():
        df = data()
        
        if df.empty:
            return ui.p(
                f"No {card_type} transactions found. Run the pipeline first:",
                ui.tags.code("uv run python -m pipeline.run"),
                style="padding: 20px; color: #666;"
            )
        
        display_df = df[["date", "description", "amount", "card_name"]].copy()
        display_df.columns = ["Date", "Description", "Amount", "Card"]
        
        gt_table = (
            GT(display_df)
            .fmt_currency(columns="Amount", currency="MXN")
            .tab_header(title=f"{card_type.title()} Transactions")
        )
        
        return ui.HTML(gt_table.as_raw_html())
    
    @render.text
    def summary():
        df = data()
        if df.empty:
            return ""
        
        total = df["amount"].sum()
        count = len(df)
        return f"Total: {count} transactions | Sum: ${total:,.2f} MXN"
