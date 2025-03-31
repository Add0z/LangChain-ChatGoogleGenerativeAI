import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import shutil

from langchain_community.vectorstores import FAISS


class WebVectorHelper:
    def __init__(self):
        """Initialize the WebVectorHelper with embedding model."""
        # Use the latest available embedding model
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_store_path = "web_faiss_index"

    def get_web_text(self, urls):
        """
        Extract text content from a list of URLs.

        Args:
            urls (list): List of URL strings to extract text from

        Returns:
            list: List of Document objects containing the extracted text
        """
        try:
            documents = []
            for url in urls:
                # Create a WebBaseLoader for the URL
                loader = WebBaseLoader(url)
                # Load the documents (web pages)
                url_docs = loader.load()
                documents.extend(url_docs)

            return documents
        except Exception as e:
            st.error(f"Error extracting text from URLs: {e}")
            return []

    @staticmethod
    def get_text_chunks(documents):
        """
        Split documents into manageable chunks for embedding.

        Args:
            documents (list): List of Document objects

        Returns:
            list: List of text chunks
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=300,
            length_function=len,
        )
        chunks = text_splitter.split_documents(documents)
        return chunks

    def get_vector_store(self, chunks):
        """
        Create a FAISS vector store from document chunks.

        Args:
            chunks (list): List of document chunks

        Returns:
            FAISS: The FAISS vector store object
        """
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        vector_store.save_local(self.vector_store_path)
        return vector_store

    def get_relevant_documents(self, question):
        """
        Retrieve documents relevant to a query from the vector store.

        Args:
            question (str): The query to search for

        Returns:
            list: List of relevant document chunks
        """
        try:
            # Check if the FAISS index exists
            if not os.path.exists(self.vector_store_path):
                st.toast("No web documents have been processed yet.", icon="🚨")
                return []

            # If index exists, proceed with similarity search
            web_db = FAISS.load_local(self.vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
            docs = web_db.similarity_search(question)
            return docs
        except Exception as e:
            st.error(f"Error retrieving web documents: {e}")
            return []

    def process_urls(self, urls):
        """
        Process a list of URLs and create a vector store from their content.

        Args:
            urls (list): List of URL strings to process
        """
        try:
            # Extract text from URLs
            web_documents = self.get_web_text(urls)

            if not web_documents:
                st.error("Failed to extract content from the provided URLs.")
                return

            # Split documents into chunks
            text_chunks = self.get_text_chunks(web_documents)

            # Create and save vector store
            self.get_vector_store(text_chunks)

            # Provide feedback
            st.success(f"Processed {len(urls)} URL(s) successfully")

        except Exception as e:
            st.error(f"Error processing URLs: {e}")

    def clear_vector_store(self, message=False):
        """
        Clear the FAISS index for web content.

        Args:
            message (bool): Whether to show a success message
        """
        try:
            # Remove the local FAISS index file if it exists
            if 'web_urls' in st.session_state:
                st.session_state.web_urls = []

            if os.path.exists(self.vector_store_path):
                shutil.rmtree(self.vector_store_path)
                if message:
                    st.success("Web documents and vector store have been cleared.")
        except Exception as e:
            st.error(f"Error clearing web vector store: {e}")