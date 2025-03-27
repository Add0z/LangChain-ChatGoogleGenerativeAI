import streamlit as st
from GeminiHelper import GeminiHelper
from ChatHistoryManager import ChatHistoryManager
from ChatRenderer import ChatRenderer
from PdfVectorHelper import PdfVectorHelper

class ChatApplication:
    def __init__(self):
        self.chat_manager = ChatHistoryManager()
        self.pdf_vector_helper = PdfVectorHelper()
        self.gemini_helper = GeminiHelper()

    def _render_clear_chat_button(self):
        """Render button to clear chat history and vector store."""
        if st.button("Clear Chat History and Uploaded PDFs"):
            # Clear chat history
            self.chat_manager.clear_chat_history()

            # Clear vector store
            self.pdf_vector_helper.clear_vector_store(True)

            # Reset input
            st.session_state.input_holder = ''

            # Clear the file uploader state
            if 'uploaded_files' in st.session_state:
                del st.session_state['uploaded_files']

            # Rerun to refresh the UI
            st.rerun()


    def _process_user_input(self, input_text):
        """Process and handle user input."""
        try:
            # Add user message to chat history
            self.chat_manager.add_message("User", input_text)
            self.chat_manager.render_chat_history()

            # Get related chunks from the vector store
            docs = self.pdf_vector_helper.get_relevant_documents(input_text)

            # Get AI response
            if not docs:
                # Use direct Gemini response for general questions
                response = self.gemini_helper.get_gemini_response(input_text)
            else:
                # Create the conversational chain
                chain = self.gemini_helper.get_conversational_chain()

                # Get response using the chain
                response = chain(
                    {"input_documents": docs,
                     "question": input_text,
                     "chat_history": self.chat_manager.get_chat_history()},
                    return_only_outputs=True
                )

                # Extract the output text
                full_response = response["output_text"]

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
        st.session_state.input_holder = st.session_state['input']
        st.session_state['input'] = ''

    def _mark_clicked(self):
        """Mark the submit button as clicked."""
        st.session_state.clicked = True
