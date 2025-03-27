import random

import streamlit as st
import time


class ChatRenderer:
    @staticmethod
    def render_message(role: str, text: str, typing_effect: bool = True):
        """
        Render a chat message with optional typing simulation.

        Args:
            role (str): The sender of the message (e.g., 'User', 'AI')
            text (str): The message text
            typing_effect (bool): Whether to simulate typing
        """
        if typing_effect:
            ChatRenderer._render_with_typing(role, text)
        else:
            ChatRenderer._render_static(role, text)

    @staticmethod
    def _render_static(role: str, text: str):
        if role == "User":
            """Render message without typing effect."""
            st.markdown(f"""
                <div style="
                    display: block;
                    background-color: #e6ffe6; 
                    border-radius: 10px; 
                    padding: 10px; 
                    margin: 5px 0;
                    color: black;
                    text-align: right;
                    width: fit-content;
                    margin-left: auto;
                ">
                    <strong>{role}:</strong> {text}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="
                    text-align: left; 
                    background-color: #e6f2ff; 
                    border-radius: 10px; 
                    padding: 10px; 
                    margin: 5px 0;
                    max-width: 80%;
                    color: black;
                    width: fit-content;
                    soft-wrap: break-word;
                ">
                    <strong>{role}:</strong> {text}
                </div>
                """, unsafe_allow_html=True)

    @staticmethod
    def _render_with_typing(role: str, text: str, typing_speed: float = 0.015):
        """
        Render message with typing simulation.

        Args:
            role (str): The sender of the message
            text (str): The message text
            typing_speed (float): Delay between each character (in seconds)
        """
        # Create a placeholder for the typing effect
        placeholder = st.empty()

        # Style configuration for the message container
        message_style = {
            "text-align": "left",
            "background-color": "#e6f2ff",
            "border-radius": "10px",
            "padding": "10px",
            "margin": "5px 0",
            "max-width": "80%",
            "color": "black",
            "width": "fit-content",
            "word-wrap": "break-word"
        }

        # Combine base styling with dynamic content
        def generate_styled_message(current_text):
            return f"""
            <div style="{'; '.join(f'{k}: {v}' for k, v in message_style.items())}">
                <strong>{role}:</strong> {current_text}
            </div>
            """

        # Simulate typing
        displayed_text = ""
        for char in text:
            displayed_text += char
            # Update placeholder with current text
            placeholder.markdown(
                generate_styled_message(displayed_text),
                unsafe_allow_html=True
            )
            # Optional: Add slight randomness to typing speed
            time.sleep(typing_speed + random.uniform(-0.005, 0.005))

        # Ensure final text is fully displayed
        placeholder.markdown(
            generate_styled_message(text),
            unsafe_allow_html=True
        )


# Example usage in a Streamlit app
def main():
    st.title("Typing Effect Demo")

    # Simulate AI typing
    ChatRenderer.render_message(
        role="AI",
        text="Hello! I'm simulating a typing effect in Streamlit. Pretty cool, right?"
    )

    # Optional: Static message rendering
    ChatRenderer.render_message(
        role="User",
        text="This is a static message without typing.",
        typing_effect=False
    )


if __name__ == "__main__":
    main()