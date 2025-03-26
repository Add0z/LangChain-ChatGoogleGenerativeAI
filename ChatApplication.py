import streamlit as st
from GeminiHelper import get_gemini_response
from ChatHistoryManager import ChatHistoryManager

from ChatRenderer import ChatRenderer


class ChatApplication:
    def __init__(self):
        self._initialize_page_config()
        self._initialize_session_state()
        self.chat_manager = ChatHistoryManager()

    def _initialize_page_config(self):
        """Set up page configuration and header."""
        st.set_page_config(page_title="LangChain Chat with Google Generative AI", layout="wide")
        st.header("LangChain Chat with Google Generative AI")

    def _initialize_session_state(self):
        """Initialize and manage session state variables."""
        default_states = {
            'something': '',
            'clicked': False,
            'input': ''
        }
        for key, default_value in default_states.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    def _render_clear_chat_button(self):
        """Render button to clear chat history."""
        if st.button("Clear Chat History"):
            self.chat_manager.clear_chat_history()
            st.session_state.something = ''

    def _process_user_input(self, input_text):
        """Process and handle user input."""
        try:
            # Add user message to chat history
            self.chat_manager.add_message("User", input_text)
            self.chat_manager.render_chat_history()

            # Get AI response
            response = get_gemini_response(input_text)
            response.resolve()
            full_response = response.text.replace('</div>', '').strip()

            # Add AI message to chat history
            self.chat_manager.add_message("AI", full_response)
            ChatRenderer.render_message("AI", full_response, True)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    def _create_input_interface(self):
        """Create input interface for chat."""
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
        st.text_input(
            "Enter your question:",
            placeholder="Ask a question...",
            key="input",
            on_change=self._update_input
        )
        st.button("Submit", on_click=self._mark_clicked)

    def _update_input(self):
        """Update session state with input text."""
        st.session_state.something = st.session_state['input']
        st.session_state['input'] = ''

    def _mark_clicked(self):
        """Mark the submit button as clicked."""
        st.session_state.clicked = True

    def run(self):
        """Main application runner."""
        # Clear chat history button
        self._render_clear_chat_button()

        # Response and input containers
        with st.container():
            st.subheader("Chat History:")
            with st.container():
                # Process input if available
                input_text = st.session_state['something']
                if input_text:
                    self._process_user_input(input_text)

                # Render input interface
                self._create_input_interface()