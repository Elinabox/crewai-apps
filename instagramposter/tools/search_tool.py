import json
import os

import requests
from langchain.tools import tool

from langchain.tools import DuckDuckGoSearchRun


class SearchTools():

    @tool("Search internet")
    def search_internet(query):
        """Useful to search the internet about a given topic and return relevant
        results."""
        # change query into a string
        queryargument = str(query)
        return SearchTools.search(queryargument)

    @tool("Search instagram")
    def search_instagram(query):
        """Useful to search for instagram post about a given topic and return relevant
        results."""
        query = f"site:instagram.com {query}"
        return SearchTools.search(query)

    def search(query, n_results=5):
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()['organic']
        stirng = []
        for result in results[:n_results]:
            try:
                stirng.append('\n'.join([
                    f"Title: {result['title']}", f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}", "\n-----------------"
                ]))
            except KeyError:
                next

        content = '\n'.join(stirng)
        print("\n=================== serper query ====================")
        print(query)
        return f"\nSearch result: {content}\n"

    from crewai_tools import SerperDevTool

    @tool('duckduckgo')
    def duck_search_tool(query):
        """Search tool using DuckDuckGo API."""
        print("")
        print(f"\n==================== duck Searching for: {query} =====================")
        searchobj = DuckDuckGoSearchRun()
        # search_result = DuckDuckGoSearchRun(query=query, max_results=5, verbose=True)
        search_result = searchobj.run(query)
        print("\n=====================================")
        print(f"Search Result: {search_result}")
        return search_result
