import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
import os

from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class GeminiHelper:
    def __init__(self, model=None):
        self.model = model or ChatGoogleGenerativeAI(model='gemini-2.0-flash')
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def get_conversational_chain(self):
        """
        Create a conversational chain with a predefined prompt template.

        Returns:
            A LangChain question-answering chain
        """
        prompt_template = """
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
           """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question", "chat_history"]
        )

        chain = load_qa_chain(self.model, chain_type="stuff", prompt=prompt)
        return chain

    def get_gemini_response(self, question):
        """
        Generate a response from the Gemini AI model.

        Args:
            question (str): The input question or prompt.

        Returns:
            str: The generated response text, or error message if generation fails.
        """
        try:
            # Send message and get the response
            response = self.model.send_message(question)
            return response.text
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"I'm sorry, but I couldn't generate a response. Error: {e}"