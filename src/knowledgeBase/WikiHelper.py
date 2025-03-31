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
            # Perform the search
            print(f"Searching Wikipedia for: {query}")
            search_results = wikipedia.search(query, results=3, suggestion=False)

            if search_results:
                # Attempt to fetch the summary of the most relevant page
                first_result = search_results[0]

                try:
                    # Get the summary for the first search result
                    summary = wikipedia.summary(first_result, sentences=3, auto_suggest=False)
                    return f"Closest Wikipedia match for '{query}':\n{summary}\n\n" + \
                        f"Other related search results:\n" + \
                        "\n".join(f"- {result}" for result in search_results[1:3])
                except wikipedia.exceptions.DisambiguationError as e:
                    # Handle disambiguation (multiple options for the query)
                    return f"Multiple possible matches found. Please be more specific.\nOptions: {', '.join(e.options[:3])}"
                except wikipedia.exceptions.RedirectError:
                    return f"The page for '{first_result}' has been redirected. Please check the page title."
                except wikipedia.exceptions.HTTPTimeoutError:
                    return "Request timed out. Please try again later."
                except wikipedia.exceptions.PageError:
                    return f"No detailed information found for '{first_result}'."
                except Exception as e:
                    return f"Error fetching summary for '{first_result}': {str(e)}"
            else:
                return f"No Wikipedia entries found for '{query}'. Please try a different search term."

        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"