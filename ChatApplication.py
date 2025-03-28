import streamlit as st
from GeminiHelper import GeminiHelper
from ChatHistoryManager import ChatHistoryManager
from ChatRenderer import ChatRenderer
from PdfVectorHelper import PdfVectorHelper
from InputCleaner import InputCleaner

class ChatApplication:
    def __init__(self):
        self.chat_manager = ChatHistoryManager()
        self.pdf_vector_helper = PdfVectorHelper()
        self.gemini_helper = GeminiHelper()
        self.cleaner = InputCleaner()

    def render_clear_chat_button(self):
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

    def process_user_input(self, input_text):
        """Process and handle user input."""
        try:
            print(input_text)
            print(st.session_state)
            clean_input = self.cleaner.clean_input(input_text)
            # Add user message to chat history
            self.chat_manager.add_message("User", input_text) # preserver the original input for display
            self.chat_manager.render_chat_history()

            # Get related chunks from the vector store
            docs = self.pdf_vector_helper.get_relevant_documents(clean_input)

            # Get AI response
            if not docs:
                # Use direct Gemini response for general questions
                response = self.gemini_helper.get_gemini_response(question=clean_input,
                                                                  chat_history=self.chat_manager.get_chat_history())
            else:
                # Create the conversational chain
                chain = self.gemini_helper.create_rag_chain()
                response = chain.invoke({
                    "context": docs,
                    "question": clean_input,
                    "chat_history": self.chat_manager.get_chat_history()
                })

            # Add AI message to chat history
            self.chat_manager.add_message("AI", response)
            ChatRenderer.render_message("AI", response, True)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    def create_input_interface(self):
        """Create input interface for chat."""
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

        st.text_input(
            "Enter your question:",
            placeholder="Ask a question...and press ENTER",
            key="input",
            on_change=self._handle_input_submission
        )

    def _handle_input_submission(self):
        """Handle input submission for both ENTER and Submit button."""
        if st.session_state['input']:
            st.session_state.input_holder = st.session_state['input']
            st.session_state['input'] = ''
            st.session_state.clicked = True
