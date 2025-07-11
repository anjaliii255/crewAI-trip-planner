from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import requests
from bs4 import BeautifulSoup
import json

class SearchInput(BaseModel):
    """Input for search tool."""
    query: str = Field(..., description="The search query")

class SearchInternetTool(BaseTool):
    name: str = "search_internet"
    description: str = "Search the internet for the given query and return top results."
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        """Perform the search logic."""
        try:
            headers = {
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/91.0.4472.124 Safari/537.36'
                )
            }
            response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract simplified top 5 results
            results = []
            for result in soup.find_all('div', class_='g')[:5]:
                title = result.find('h3')
                if title:
                    results.append(title.text)

            return json.dumps(results)

        except Exception as e:
            return f"Error during search: {str(e)}"