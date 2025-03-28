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
    def __init__(self, model_name='gemini-2.0-flash'):
        """
        Initialize the GeminiHelper with a specific model.

        Args:
            model_name (str, optional): Name of the Gemini model to use.
            Defaults to 'gemini-pro'.
        """
        # Use ChatGoogleGenerativeAI wrapper instead of direct GenerativeModel
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            convert_system_message_to_human=True
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def create_rag_chain(self):
        """
        Create a modern Retrieval-Augmented Generation (RAG) chain.

        Returns:
            A LangChain RAG chain for question-answering
        """
        # Define the prompt template
        prompt_template = ChatPromptTemplate.from_template(
            """
               Answer the following questions as detailed as possible from the provided context and chat_history,
                make sure to provide the answer in the same language as the question.
                make sure to use the same language as the question.
                make sure to provide the correct answer.
                if you don't know the answer, just say that you don't know, don't try to make up an answer.
                if you need to use the context and chat_history, use it to answer the question.
                if you need more context, ask for it.
                make sure to explicitly mention when your answer is based on the context and chat_history or based on your own knowledge.
                Chat History: \n {chat_history} \n
                Context: \n {context} \n
                Question: \n {question} \n

                Answer:
           """)

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
            model = genai.GenerativeModel('gemini-2.0-flash')

            # If context is provided, prepend it to the question
            if context:
                full_query = f"Context: {context}\n\nQuestion: {question}"
            else:
                full_query = question

            # Generate the response
            response = model.generate_content(full_query)

            return response.text
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"I'm sorry, but I couldn't generate a response. Error: {e}"