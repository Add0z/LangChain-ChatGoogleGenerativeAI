import streamlit as st
from src.knowledgeBase.WebVectorHelper import WebVectorHelper


class WebSideBar:
    def __init__(self):
        self.web_vector_helper = WebVectorHelper()

        # Initialize session state variables if not exist
        if 'processing_web' not in st.session_state:
            st.session_state.processing_web = False

        if 'hasNoWeb' not in st.session_state:
            st.session_state.hasNoWeb = True

        if 'web_urls' not in st.session_state:
            st.session_state.web_urls = []

        if 'url_input' not in st.session_state:
            st.session_state.url_input = ''

    def _handle_url_input(self):
        """Handle URL input change."""
        if st.session_state['url_input']:
            st.session_state.web_holder = st.session_state['url_input']
            st.session_state['url_input'] = ''
            st.session_state.clicked = True

    def render(self):
        """Render the Web sidebar section"""
        st.subheader("Web Content")

        # URL input - only disabled during processing
        url_input = st.text_input(
            "Enter URL:",
            disabled=st.session_state.processing_web,
            key="url_input_field",  # Changed key to avoid conflicts
            placeholder="Enter URL..."
        )

        # Add URL button
        if st.button("Add URL", key="add_url_button", disabled=st.session_state.processing_web):
            # Strip whitespace and check URL
            cleaned_url = url_input.strip() if url_input else ""
            if cleaned_url and (cleaned_url.startswith("http://") or cleaned_url.startswith("https://")):
                if cleaned_url not in st.session_state.web_urls:
                    st.session_state.web_urls.append(cleaned_url)
                    # Don't modify session state directly for the widget
                    st.rerun()
            else:
                st.warning(f"Please enter a valid URL starting with http:// or https://")

        # Display added URLs
        if st.session_state.web_urls:
            st.write("Added URLs:")
            for i, url in enumerate(st.session_state.web_urls):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.text(f"{i + 1}. {url}")
                with col2:
                    if st.button("❌", key=f"remove_url_{i}", disabled=st.session_state.processing_web):
                        st.session_state.web_urls.pop(i)
                        st.rerun()

        # Process URLs button
        if st.button("Process URLs",
                     disabled=(not st.session_state.web_urls or st.session_state.processing_web),
                     key='process_web_button'):
            st.session_state.processing_web = True
            st.rerun()

        # If processing web is true, run the actual processing
        if st.session_state.processing_web:
            try:
                with st.spinner("Processing Web Content..."):
                    self.web_vector_helper.process_urls(st.session_state.web_urls)
                # Set a success flag before rerun
                st.session_state.processing_web_success = True
            except Exception as e:
                st.error(f"Web processing failed: {e}")
            finally:
                # Always reset processing state
                st.session_state.processing_web = False
                st.session_state.hasNoWeb = False
                st.rerun()

        # Check for web success message after rerun
        if st.session_state.get('processing_web_success', False):
            st.success("Web content processing completed successfully!")
            # Clear the success flag
            st.session_state.processing_web_success = False

        # Clear vector stores if no content and not processing
        if not st.session_state.web_urls and not st.session_state.processing_web:
            self.web_vector_helper.clear_vector_store(False)