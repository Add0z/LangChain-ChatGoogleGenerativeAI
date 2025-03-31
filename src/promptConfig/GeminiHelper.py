import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class GeminiHelper:
    def __init__(self, model_name='gemini-2.0-flash', temperature=0.5):
        """
        Initialize the GeminiHelper with a specific model.

        Args:
            model_name (str, optional): Name of the Gemini model to use.
            Defaults to 'gemini-2.0-flash'.
        """
        # Use ChatGoogleGenerativeAI wrapper instead of direct GenerativeModel
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            convert_system_message_to_human=True
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.temperature = temperature

    def create_rag_chain(self):
        """
        Create a modern Retrieval-Augmented Generation (RAG) chain.

        Returns:
            A LangChain RAG chain for question-answering
        """

        prompt_template = ChatPromptTemplate.from_template("""You are an AI assistant that provides precise and accurate answers.
            Always answer in the same language as the question.
            If asked in Portuguese, answer in Portuguese.

            Follow these guidelines carefully:
            1. If the context provides relevant information, use it to form your answer.
            2. Always be clear about the source of your information:
               - If using context, mention "Based on the provided documents:"
               - If using general knowledge, mention "Based on my general knowledge:"
            3. If the context does not contain sufficient information to answer the question, 
               clearly state this and offer to help find more information.
            4. Answer in the same language as the question.
            5. Be concise but comprehensive.
            6. If the question is not clear, ask for clarification.
            7. Do not correct any grammar or spelling mistakes, even if they are minor.
            8. Keep your answers short and precise.

            Chat History: \n {chat_history} \n
            Context: \n {context} \n
            Question: \n {question} \n

            Answer:
            """
        )

        # Create the RAG chain
        rag_chain = (
                RunnablePassthrough.assign(
                    input_documents=lambda x: x.get("context", []),
                    question=lambda x: x.get("question", ""),
                    chat_history=lambda x: x.get("chat_history", [])
                )
                | prompt_template
                | self.model
                | StrOutputParser()
        )

        return rag_chain

    def get_gemini_response(self, question, context=None, chat_history=None):
        """
        Generate a response using Gemini's full knowledge base.

        Args:
            question (str): The input question
            context (str, optional): Additional context to supplement the answer
            chat_history (list, optional): Previous conversation history

        Returns:
            str: The generated response text
        """
        try:
            # Import genai directly to ensure we have the correct module
            import google.generativeai as genai

            # Configure the API key again to ensure it's set
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

            # Create a generative model
            model = genai.GenerativeModel('gemini-2.0-flash',generation_config={"temperature": self.temperature})

            # Construct a comprehensive prompt that includes context, chat history, and question
            full_query_parts = []

            template = (
                """You are an AI assistant that provides precise and accurate answers.
                Always answer in the same language as the question.
                If asked in Portuguese, answer in Portuguese.
                Follow these guidelines carefully:
                1. If the context provides relevant information, use it to form your answer.
                2. Always be clear about the source of your information:
                  - If using context, mention "Based on the provided documents:"
                  - If using general knowledge, mention "Based on my general knowledge:"
                3. If the context does not contain sufficient information to answer the question, 
                  clearly state this and offer to help find more information.
                4. Answer in the same language as the question.
                5. Be concise but comprehensive.
                6. If the question is not clear, ask for clarification.
                7. Do not correct any grammar or spelling mistakes, even if they are minor.
                8. Keep your answers short and precise.
                """
            )

            full_query_parts.append(template)
            # Add context if provided
            if context:
                full_query_parts.append(f"Context: {context}")

            # Add chat history if provided and it's a list of dictionaries
            if chat_history:
                # Safely handle different chat history formats
                if isinstance(chat_history, list):
                    print("chat_history is list")
                    try:
                        # Try to extract text from dictionary-style chat history
                        history_str = "\n".join([
                            f"{msg.get('role', 'Unknown')}: {msg.get('parts', [msg.get('content', 'No message')])}"
                            for msg in chat_history[-3:]
                        ])
                    except Exception:
                        # Fallback to string representation if dictionary access fails
                        history_str = "\n".join(str(msg) for msg in chat_history[-3:])

                    full_query_parts.append(f"Previous Conversation:\n{history_str}")
                elif isinstance(chat_history, str):
                    print("chat_history is string")
                    # If chat_history is already a string
                    full_query_parts.append(f"Previous Conversation:\n{chat_history}")

            # Add the main question
            full_query_parts.append(f"Question: {question}")
            full_query_parts.append("Please provide a comprehensive answer.")

            # Join all parts
            full_query = "\n\n".join(full_query_parts)

            # Generate the response
            response = model.generate_content(full_query)

            return response.text
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"I'm sorry, but I couldn't generate a response. Error: {e}"