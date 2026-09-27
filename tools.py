from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for the given query and return title, URLs and content summary of the results."""
    try:
        response = tavily_client.search(query = query, max_results = 5)
        results = []
        for res in response["results"]:
            results.append({
                "title": res["title"],
                "url": res["url"],
                "content": res["content"][:200]  # Return a summary of the content (first 200 characters)
            })
        return results
    except Exception as e:
        return f"An error occurred while searching: {str(e)}"
    

@tool
def scrape_url(url:str) -> str:
    """Scrape the content of the given URL and return the text."""
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()  
        return soup.get_text(separator=' ', strip=True)[:3000]  
    except Exception as e:
        return f"An error occurred while scraping: {str(e)}"
    