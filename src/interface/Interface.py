import streamlit as st
from src.interface.ChatApplication import ChatApplication
from src.interface.chat.ChatHistoryManager import ChatHistoryManager
from src.interface.chat.InputCleaner import InputCleaner
from src.interface.PdfSideBar import PdfSideBar
from src.interface.WebSideBar import WebSideBar
import base64



class Interface:
    def __init__(self):
        """Initialize the interface with the chat application."""
        self.app = ChatApplication()
        self.chat_manager = ChatHistoryManager()
        self.pdf_sidebar = PdfSideBar()
        self.web_sidebar = WebSideBar()
        self.cleaner = InputCleaner()
        self._initialize_page_config()
        self._initialize_session_state()

    @staticmethod
    def _initialize_page_config():
        """Set up page configuration and header."""
        st.set_page_config(page_title="LangChain Chat with Google Generative AI", layout="wide")
        st.header("LangChain Chat with Google Generative AI")

        # Function to encode image
        def get_base64_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()

        image_path = "src/interface/utils/img.png"  # Update if necessary
        base64_img = get_base64_image(image_path)

        # Apply custom CSS for background image
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{base64_img}");
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def _initialize_session_state():
        """Initialize and manage session state variables."""
        default_states = {
            'input_holder': '',
            'web_holder': '',
            'clicked': False,
            'input': ''
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

            # Render PDF sidebar section
            self.pdf_sidebar.render()

            # Add some spacing between sections
            st.markdown("---")

            # Render Web sidebar section
            self.web_sidebar.render()


def main():
    """Entry point for the Streamlit application."""
    interface = Interface()
    interface.run()


if __name__ == "__main__":
    main()