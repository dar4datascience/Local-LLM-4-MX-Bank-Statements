from shiny import App, ui
from modules.transactions_table import transactions_table_ui, transactions_table_server
from modules.chat_assistant import chat_assistant_ui, chat_assistant_server


app_ui = ui.page_navbar(
    ui.nav_panel(
        "Credit Cards",
        ui.layout_columns(
            transactions_table_ui("credit_table", "Credit"),
            col_widths=12
        )
    ),
    ui.nav_panel(
        "Debit Cards",
        ui.layout_columns(
            transactions_table_ui("debit_table", "Debit"),
            col_widths=12
        )
    ),
    ui.nav_spacer(),
    ui.nav_panel(
        "Chat Assistant",
        ui.layout_columns(
            chat_assistant_ui("chat_module"),
            col_widths=12
        )
    ),
    title="MX Bank Statements Dashboard",
    id="navbar"
)


def server(input, output, session):
    transactions_table_server("credit_table", card_type="credit")
    transactions_table_server("debit_table", card_type="debit")
    chat_assistant_server("chat_module")


app = App(app_ui, server)
