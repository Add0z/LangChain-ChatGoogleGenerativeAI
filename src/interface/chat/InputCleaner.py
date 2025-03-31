import os
import re
import nltk


class InputCleaner:
    def __init__(self):
        """
        Initialize the InputCleaner with robust stop words handling.
        """
        # SSL Certificate Bypass
        try:
            import ssl
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        # Download NLTK resources
        self._download_nltk_resources()

        # Predefined fallback stop words
        self.default_stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'were', 'will', 'with'
        }

        # Try to load NLTK stop words with fallback
        try:
            from nltk.corpus import stopwords
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            print("Falling back to default stop words list.")
            self.stop_words = self.default_stop_words

    def _download_nltk_resources(self):
        """
        Attempt to download NLTK resources with multiple fallback strategies.
        """
        # Determine potential download directories
        potential_dirs = [
            os.path.join(os.path.expanduser('~'), 'nltk_data'),
            '/usr/local/share/nltk_data',
            '/usr/share/nltk_data'
        ]

        # Try to create a download directory if it doesn't exist
        for download_dir in potential_dirs:
            try:
                os.makedirs(download_dir, exist_ok=True)
                nltk.data.path.append(download_dir)
            except Exception:
                continue

        # List of resources to download
        resources = ['stopwords', 'punkt']

        for resource in resources:
            try:
                nltk.download(resource, quiet=True)
            except Exception as e:
                print(f"Warning: Could not download {resource}: {e}")

    def normalize_text(self, text):
        """
        Normalize text by converting to lowercase.

        Args:
            text (str): Input text to normalize

        Returns:
            str: Normalized text
        """
        return text.lower() if text else ""

    def remove_special_characters(self, text):
        """
        Remove special characters while preserving certain punctuation.

        Args:
            text (str): Input text to clean

        Returns:
            str: Cleaned text
        """
        # Keep certain punctuation and formatting
        text = re.sub(r'[^\w\s:?.,!]', '', text)

        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def remove_stopwords(self, text):
        """
        Carefully remove stop words while preserving question structure.

        Args:
            text (str): Input text to remove stop words from

        Returns:
            str: Text with less important stop words removed
        """
        # Split into words
        tokens = text.split()

        # Preserve important words and question structure
        preserved_tokens = []
        for word in tokens:
            # Keep words that might be crucial to the question's meaning
            if word.lower() not in self.stop_words or len(word) > 3:
                preserved_tokens.append(word)

        return ' '.join(preserved_tokens)

    def clean_input(self, text):
        """
        Comprehensive input cleaning method with careful preservation.

        Args:
            text (str): Raw input text

        Returns:
            str: Fully cleaned and processed text
        """
        if not text:
            return ""

        # Apply cleaning steps in sequence
        cleaned_text = text

        # Normalize text (lowercase)
        cleaned_text = self.normalize_text(cleaned_text)

        # Remove special characters (but keep some punctuation)
        cleaned_text = self.remove_special_characters(cleaned_text)

        # Carefully remove stop words
        cleaned_text = self.remove_stopwords(cleaned_text)

        return cleaned_text