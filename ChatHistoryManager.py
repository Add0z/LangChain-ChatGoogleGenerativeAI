import streamlit as st

from ChatRenderer import ChatRenderer

class ChatHistoryManager:
    def __init__(self, session_state_key='chat_history'):
        """
        Initialize the ChatHistoryManager.

        Args:
            session_state_key (str): Key to use in st.session_state for chat history
        """
        self.session_state_key = session_state_key

        # Initialize chat history if not exists
        if self.session_state_key not in st.session_state:
            st.session_state[self.session_state_key] = []

    def add_message(self, role, text):
        """
        Add a message to the chat history and immediately render it.

        Args:
            role (str): Role of the message sender (User/AI)
            text (str): Message text
        """
        # Add message to session state
        st.session_state[self.session_state_key].append((role, text))

    def get_chat_history(self):
        """
        Retrieve the current chat history.

        Returns:
            list: List of tuples containing (role, text) for each message
        """
        return st.session_state[self.session_state_key]

    def clear_chat_history(self):
        """
        Clear the entire chat history.
        """
        st.session_state[self.session_state_key] = []

    def render_chat_history(self):
        """
        Render the entire chat history.
        """
        for role, text in self.get_chat_history():
            ChatRenderer.render_message(role, text,False)