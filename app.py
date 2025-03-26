import streamlit as st

from ChatApplication import ChatApplication
from GeminiHelper import get_gemini_response
from ChatHistoryManager import ChatHistoryManager


def main():
    """Entry point for the Streamlit application."""
    app = ChatApplication()
    app.run()

if __name__ == "__main__":
    main()