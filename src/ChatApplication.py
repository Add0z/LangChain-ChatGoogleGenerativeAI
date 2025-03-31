import streamlit as st

from src.ChatHistoryManager import ChatHistoryManager
from src.ChatRenderer import ChatRenderer
from src.GeminiHelper import GeminiHelper
from src.InputCleaner import InputCleaner
from src.PdfVectorHelper import PdfVectorHelper
from src.WikiHelper import WikiHelper


class ChatApplication:
    def __init__(self):
        self.chat_manager = ChatHistoryManager()
        self.pdf_vector_helper = PdfVectorHelper()
        self.gemini_helper = GeminiHelper()
        self.cleaner = InputCleaner()
        self.wiki_helper = WikiHelper()


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
        """Process and handle user input based on selected toggles."""
        try:
            clean_input = self.cleaner.clean_input(input_text)
            # Add user message to chat history
            self.chat_manager.add_message("User", input_text)  # preserve the original input for display
            self.chat_manager.render_chat_history()

            # Determine response generation method based on toggles

            if st.session_state.wikipedia_toggle:
                # Wikipedia-based response
                st.toast("Your questions will be answered using Wikipedia.", icon="🌐")
                response = self.wiki_helper.search_wikipedia(input_text)
                emoji = "🌐AI"

            elif st.session_state.internet_toggle:
                # Internet-based response
                st.toast("Your questions will be answered using the internet.", icon="🛜")
                response = self.gemini_helper.get_gemini_response(
                    question=clean_input,
                    chat_history=self.chat_manager.get_chat_history()
                )
                emoji = "🛜AI"

            elif st.session_state.pdfs_toggle and not st.session_state.hasNoPdf:
                # PDF-based RAG response
                st.toast("Your questions will be answered based on the PDFs.", icon="📂")
                # Get related chunks from the vector store
                docs = self.pdf_vector_helper.get_relevant_documents(clean_input)

                if docs:
                    # Create the conversational chain
                    chain = self.gemini_helper.create_rag_chain()
                    response = chain.invoke({
                        "context": docs,
                        "question": clean_input,
                        "chat_history": self.chat_manager.get_chat_history()
                    })
                    emoji = "📂AI"
                else:
                    # Fallback to internet response if no relevant docs found
                    response = self.gemini_helper.get_gemini_response(
                        question=clean_input,
                        chat_history=self.chat_manager.get_chat_history()
                    )
                    emoji = "🛜AI"
                    st.warning("No relevant PDF context found. Using internet-based response.")

            else:
                # Default to internet response if no toggle is selected
                st.toast("Your questions will be answered using the internet.", icon="🛜")
                response = self.gemini_helper.get_gemini_response(
                    question=clean_input,
                    chat_history=self.chat_manager.get_chat_history()
                )
                emoji = "🛜AI"
                st.session_state.internet_toggle = True

            # Add AI message to chat history
            self.chat_manager.add_message(emoji, response)
            ChatRenderer.render_message(emoji, response, True)

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
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

        with col1:
            st.toggle("🛜 Use internet",
                      key="internet_toggle",
                      value=st.session_state.hasNoPdf,
                      disabled=st.session_state.hasNoPdf)
        with col2:
            st.toggle("📃 Use PDFs",
                      key="pdfs_toggle",
                      value=not st.session_state.hasNoPdf,
                      disabled=st.session_state.hasNoPdf)
        with col3:
            st.toggle("🌐 Use Wikipedia(beta)", key="wikipedia_toggle")


    @staticmethod
    def _handle_input_submission():
        """Handle input submission for both ENTER and Submit button."""
        if st.session_state['input']:
            st.session_state.input_holder = st.session_state['input']
            st.session_state['input'] = ''
            st.session_state.clicked = True