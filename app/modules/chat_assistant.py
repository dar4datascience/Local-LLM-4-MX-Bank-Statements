from shiny import module, ui, render, reactive
import ollama
from ..db import get_db_schema


@module.ui
def chat_assistant_ui():
    """UI for chat assistant module."""
    return ui.card(
        ui.card_header("💬 Ask about your spending"),
        ui.layout_column_wrap(
            ui.input_text_area("user_input", "Ask a question:", width="100%", rows=3),
            ui.input_action_button("send", "Send", class_="btn-primary"),
            width=1
        ),
        ui.output_text_verbatim("response", placeholder=True)
    )


@module.server
def chat_assistant_server(input, output, session):
    """Server logic for chat assistant module."""
    
    system_prompt = f"""You are a helpful financial assistant. You have access to a DuckDB database with transaction data.

{get_db_schema()}

When the user asks questions about their spending, you can:
1. Explain what data is available
2. Suggest SQL queries to answer their questions
3. Help them understand their spending patterns

Be concise and helpful. If asked to query the database, provide the SQL query they can run.
"""
    
    response_text = reactive.value("")
    
    @reactive.effect
    @reactive.event(input.send)
    def handle_chat():
        user_msg = input.user_input()
        if not user_msg.strip():
            return
        
        response_text.set("Thinking...")
        
        try:
            result = ollama.chat(
                model="llama3.2",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ]
            )
            response_text.set(result['message']['content'])
        except Exception as e:
            response_text.set(f"Error: {str(e)}")
    
    @render.text
    def response():
        return response_text.get()
