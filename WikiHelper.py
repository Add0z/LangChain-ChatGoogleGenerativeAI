import wikipedia


class WikiHelper:
    def __init__(self):
        pass

    @staticmethod
    def search_wikipedia(query):
        """
        Enhanced Wikipedia search with multiple fallback strategies.

        Args:
            query (str): Search query

        Returns:
            str: Wikipedia summary or explanation
        """
        try:
            # First, try exact page match
            try:
                summary = wikipedia.summary(query, sentences=3)
                return f"Wikipedia Summary for '{query}':\n{summary}"
            except wikipedia.exceptions.DisambiguationError as e:
                # If disambiguation, return top 3 options
                options = e.options[:3]
                return f"Your query '{query}' could refer to multiple topics. Possible matches:\n" + \
                    "\n".join(f"- {option}" for option in options)
            except wikipedia.exceptions.PageError:
                # If no exact match, try searching
                try:
                    # Search for pages
                    search_results = wikipedia.search(query, results=3)
                    if search_results:
                        # Try to get summary of the first search result
                        first_result = search_results[0]
                        summary = wikipedia.summary(first_result, sentences=3)
                        return f"Closest Wikipedia match for '{query}':\n{summary}\n\n" + \
                            f"Other related search results:\n" + \
                            "\n".join(f"- {result}" for result in search_results[1:3])
                    else:
                        return f"No Wikipedia entries found for '{query}'. Try a different search term."
                except Exception as search_error:
                    return f"Wikipedia search failed: {search_error}"
        except Exception as e:
            return f"An unexpected error occurred while searching Wikipedia: {e}"