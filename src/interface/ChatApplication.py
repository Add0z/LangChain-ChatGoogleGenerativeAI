import streamlit as st

from src.interface.chat.ChatHistoryManager import ChatHistoryManager
from src.interface.chat.ChatRenderer import ChatRenderer
from src.promptConfig.GeminiHelper import GeminiHelper
from src.interface.chat.InputCleaner import InputCleaner
from src.knowledgeBase.PdfVectorHelper import PdfVectorHelper
from src.knowledgeBase.WebVectorHelper import WebVectorHelper
from src.knowledgeBase.WikiHelper import WikiHelper


class ChatApplication:
    def __init__(self):
        self.chat_manager = ChatHistoryManager()
        self.pdf_vector_helper = PdfVectorHelper()
        self.web_vector_helper = WebVectorHelper()
        self.gemini_helper = GeminiHelper()
        self.cleaner = InputCleaner()
        self.wiki_helper = WikiHelper()

    def render_clear_chat_button(self):
        """Render button to clear chat history and vector stores."""
        if st.button("Clear Chat History and Uploaded Content"):
            # Clear chat history
            self.chat_manager.clear_chat_history()

            # Clear vector stores
            self.pdf_vector_helper.clear_vector_store(True)
            self.web_vector_helper.clear_vector_store(True)

            # Reset input
            st.session_state.input_holder = ''

            # Clear the uploaded content states
            if 'uploaded_files' in st.session_state:
                del st.session_state['uploaded_files']

            st.session_state.web_urls = []
            st.session_state.hasNoPdf = True
            st.session_state.hasNoWeb = True

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

            elif st.session_state.web_toggle and not st.session_state.hasNoWeb:
                # Web-based RAG response
                st.toast("Your questions will be answered based on the web page content.", icon="📄")
                # Get related chunks from the web vector store
                web_docs = self.web_vector_helper.get_relevant_documents(clean_input)

                if web_docs:
                    # Create the conversational chain
                    chain = self.gemini_helper.create_rag_chain()
                    response = chain.invoke({
                        "context": web_docs,
                        "question": clean_input,
                        "chat_history": self.chat_manager.get_chat_history()
                    })
                    emoji = "📄AI"
                else:
                    # Fallback to internet response if no relevant web_docs found
                    st.warning("No relevant web content found. Using internet-based response.")
                    response = self.gemini_helper.get_gemini_response(
                        question=clean_input,
                        chat_history=self.chat_manager.get_chat_history()
                    )
                    emoji = "🛜AI"
                    st.warning("No relevant web content found. Using internet-based response.")

            elif st.session_state.pdfs_toggle and not st.session_state.hasNoPdf:
                # PDF-based RAG response
                st.toast("Your questions will be answered based on the PDFs.", icon="📂")
                # Get related chunks from the vector store
                pdf_docs = self.pdf_vector_helper.get_relevant_documents(clean_input)

                if pdf_docs:
                    # Create the conversational chain
                    chain = self.gemini_helper.create_rag_chain()
                    response = chain.invoke({
                        "context": pdf_docs,
                        "question": clean_input,
                        "chat_history": self.chat_manager.get_chat_history()
                    })
                    emoji = "📂AI"
                else:
                    # Fallback to internet response if no relevant pdf_docs found
                    st.warning("No relevant PDF context found. Using internet-based response.")
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
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

        with col1:
            st.toggle("🛜 Internet",
                      key="internet_toggle",
                      value=True)
        with col2:
            st.toggle("📃 PDFs",
                      key="pdfs_toggle",
                      value=False)
        with col3:
            st.toggle("🌍 Web",
                      key="web_toggle",
                      value=False)
        with col4:
            st.toggle("🌐 Wikipedia(beta)", key="wikipedia_toggle",
                      value=False)

    @staticmethod
    def _handle_input_submission():
        """Handle input submission for both ENTER and Submit button."""
        if st.session_state['input']:
            st.session_state.input_holder = st.session_state['input']
            st.session_state['input'] = ''
            st.session_state.clicked = True