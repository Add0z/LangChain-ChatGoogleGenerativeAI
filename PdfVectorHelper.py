import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
import os
import shutil

from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


class PdfVectorHelper:
    def __init__(self):
        # Try using the latest available embedding model
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def get_pdf_text(self, pdf_docs):
        pdf_text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
        return pdf_text

    def get_text_chunks(self, pdf_text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(pdf_text)
        return chunks

    def get_vector_store(self, chunks, pdf_Id=None):
        if pdf_Id:
            vector_store = FAISS.from_texts(chunks, self.embeddings, document_id=pdf_Id)
        else:
            vector_store = FAISS.from_texts(chunks, self.embeddings)
        vector_store.save_local("faiss_index")
        return vector_store

    def get_relevant_documents(self, question):
        try:
            # Check if the FAISS index exists
            if not os.path.exists("faiss_index"):
                # If no index exists, return an empty list or raise a custom exception
                st.toast("No PDF documents have been uploaded and processed yet.",icon="🚨")
                return []

            # If index exists, proceed with similarity search
            new_db = FAISS.load_local("faiss_index", self.embeddings, allow_dangerous_deserialization=True)
            docs = new_db.similarity_search(question)
            return docs
        except Exception as e:
            st.error(f"Error retrieving documents: {e}")
            return []

    def process_pdf(self, pdf_docs):
        """
        Process uploaded PDF documents.

        Args:
            pdf_docs (list): List of PDF files to process
        """
        try:
            # Extract text from PDFs
            raw_text = self.get_pdf_text(pdf_docs)

            # Split text into chunks
            text_chunks = self.get_text_chunks(raw_text)

            # Create and save vector store
            self.get_vector_store(text_chunks)

            # Optional: Add more detailed logging or feedback
            st.success(f"Processed {len(pdf_docs)} PDF(s) successfully")

        except Exception as e:
            st.error(f"Error processing PDFs: {e}")

    def clear_vector_store(self,message=False):
        """
        Clear the FAISS index and remove the local index file.
        """
        try:
            # Remove the local FAISS index file if it exists
            st.session_state.pdf_uploads = []
            if os.path.exists("faiss_index"):
                shutil.rmtree("faiss_index")
                if message:
                    st.success("PDF documents and vector store have been cleared.")
        except Exception as e:
            st.error(f"Error clearing vector store: {e}")