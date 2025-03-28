import streamlit as st
from ChatApplication import ChatApplication
from ChatHistoryManager import ChatHistoryManager
from InputCleaner import InputCleaner

from PdfVectorHelper import PdfVectorHelper


class Interface:
    def __init__(self):
        """Initialize the interface with the chat application."""
        self.app = ChatApplication()
        self.chat_manager = ChatHistoryManager()
        self.pdf_vector_helper = PdfVectorHelper()
        self.cleaner = InputCleaner()
        self._initialize_page_config()
        self._initialize_session_state()

    @staticmethod
    def _initialize_page_config():
        """Set up page configuration and header."""
        st.set_page_config(page_title="LangChain Chat with Google Generative AI", layout="wide")
        st.header("LangChain Chat with Google Generative AI")

    @staticmethod
    def _initialize_session_state():
        """Initialize and manage session state variables."""
        default_states = {
            'input_holder': '',
            'clicked': False,
            'input': '',
            'hasNoPdf': False
        }
        for key, default_value in default_states.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    def run(self):
        """Main application runner."""
        # Clear chat history button
        self.app.render_clear_chat_button()

        # Response and input containers
        with st.container():
            st.subheader("Chat History:")
            with st.container():
                # Process input if available
                input_text = st.session_state['input_holder']
                if input_text:
                    self.app.process_user_input(input_text)
                    st.session_state.input_holder = ''
                else:
                    self.chat_manager.render_chat_history()

                # Render input interface
                self.app.create_input_interface()

        with st.sidebar:
            st.title("Menu:")

            # Initialize processing state if not exists
            if 'processing' not in st.session_state:
                st.session_state.processing = False

            # Disable file uploader when processing
            pdf_docs = st.file_uploader(
                "Upload your PDF Files and Click on the Submit & Process Button",
                accept_multiple_files=True,
                disabled=st.session_state.processing
            )

            # Process button with state management
            if st.button("Process",
                         disabled=(not pdf_docs or st.session_state.processing),
                         key='process_pdf_button'):
                # Set processing to True
                st.session_state.processing = True

                # Trigger a rerun
                st.rerun()

            # If processing is true, run the actual processing
            if st.session_state.processing:
                try:
                    with st.spinner("Processing..."):
                        self.app.pdf_vector_helper.process_pdf(pdf_docs)

                    # Set a success flag before rerun
                    st.session_state.processing_success = True
                except Exception as e:
                    st.error(f"Processing failed: {e}")
                finally:
                    # Always reset processing state
                    st.session_state.processing = False
                    st.rerun()

            # Check for success message after rerun
            if st.session_state.get('processing_success', False):
                st.success("PDF processing completed successfully!")
                # Clear the success flag
                st.session_state.processing_success = False

            # Clear vector store if no docs are uploaded
            if not pdf_docs:
                self.pdf_vector_helper.clear_vector_store(False)





def main():
    """Entry point for the Streamlit application."""
    interface = Interface()
    interface.run()

if __name__ == "__main__":
    main()