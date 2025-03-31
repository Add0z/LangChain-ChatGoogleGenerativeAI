import streamlit as st
from src.knowledgeBase.PdfVectorHelper import PdfVectorHelper


class PdfSideBar:
    def __init__(self):
        self.pdf_vector_helper = PdfVectorHelper()

        # Initialize processing state if not exists
        if 'processing_pdf' not in st.session_state:
            st.session_state.processing_pdf = False

        if 'hasNoPdf' not in st.session_state:
            st.session_state.hasNoPdf = True

    def render(self):
        """Render the PDF sidebar section"""
        st.subheader("PDF Documents")

        # Disable file uploader ONLY when processing
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button",
            accept_multiple_files=True,
            disabled=st.session_state.processing_pdf
        )

        # Process PDF button with state management
        if st.button("Process PDFs",
                     disabled=(not pdf_docs or st.session_state.processing_pdf),
                     key='process_pdf_button'):
            # Set processing to True
            st.session_state.processing_pdf = True
            # Trigger a rerun
            st.rerun()

        # If processing PDF is true, run the actual processing
        if st.session_state.processing_pdf:
            try:
                with st.spinner("Processing PDFs..."):
                    self.pdf_vector_helper.process_pdf(pdf_docs)
                # Set a success flag before rerun
                st.session_state.processing_pdf_success = True
            except Exception as e:
                st.error(f"PDF processing failed: {e}")
            finally:
                # Always reset processing state
                st.session_state.processing_pdf = False
                st.session_state.hasNoPdf = False
                st.rerun()

        # Check for PDF success message after rerun
        if st.session_state.get('processing_pdf_success', False):
            st.success("PDF processing completed successfully!")
            # Clear the success flag
            st.session_state.processing_pdf_success = False

        # Clear vector stores if no content
        if not pdf_docs and not st.session_state.processing_pdf:
            self.pdf_vector_helper.clear_vector_store(False)

        return pdf_docs