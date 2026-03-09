import os
from tavily import TavilyClient
from typing import List, Dict

import requests

def is_valid_image_url(url: str) -> bool:
    """
    Checks if a URL is a valid, accessible image.
    """
    if not url or not url.startswith("http"):
        return False
    
    try:
        # Use HEAD request to be efficient
        response = requests.head(url, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            content_type = response.headers.get("content-type", "").lower()
            return "image" in content_type or any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".svg", ".webp", ".gif"])
        
        # Fallback to GET if HEAD is not allowed
        if response.status_code in [403, 405]:
            response = requests.get(url, timeout=10, stream=True)
            return response.status_code == 200 and "image" in response.headers.get("content-type", "").lower()
            
        return False
    except Exception:
        return False

def web_search(query: str, max_results: int = 5) -> List[Dict]:
    """
    Performs a web search using Tavily.
    Args:
        query: The search query.
        max_results: Maximum number of results to return.
    Returns:
        A list of search results with titles, URLs, and snippets.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment.")
    
    tavily = TavilyClient(api_key=api_key)
    # Search for the query
    response = tavily.search(query=query, search_depth="advanced", max_results=max_results)
    
    return response.get("results", [])

def search_institution_details(name: str, country: str) -> str:
    """
    Convenience function to specifically search for institution details including images.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment.")
    
    tavily = TavilyClient(api_key=api_key)
    query = f"official website and logo image URL for {name} institution in {country}"
    
    # Advanced search with images enabled
    response = tavily.search(query=query, search_depth="advanced", max_results=5, include_images=True)
    
    results = response.get("results", [])
    images = response.get("images", [])
    
    formatted_results = "WEB SEARCH RESULTS:\n"
    for r in results:
        formatted_results += f"- Title: {r.get('title')}\n  URL: {r.get('url')}\n  Snippet: {r.get('content')}\n\n"
    
    formatted_results += "FOUND IMAGE URLS:\n"
    for img in images:
        formatted_results += f"- {img}\n"
    
    return formatted_results
