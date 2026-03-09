import os
from tavily import TavilyClient
from typing import List, Dict

import requests

def is_valid_image_url(url: str) -> bool:
    """
    Checks if a URL is a valid, accessible image.
    More permissive to handle sites that block automated requests.
    """
    if not url or not url.startswith("http"):
        return False
    
    # Common image extensions
    image_extensions = [".jpg", ".jpeg", ".png", ".svg", ".webp", ".gif"]
    is_image_ext = any(url.lower().split("?")[0].endswith(ext) for ext in image_extensions)

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    }

    try:
        # 1. Try HEAD request
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            content_type = response.headers.get("content-type", "").lower()
            return "image" in content_type or is_image_ext
        
        # 2. Try GET request if HEAD failed or was blocked
        response = requests.get(url, headers=headers, timeout=10, stream=True)
        if response.status_code == 200:
            content_type = response.headers.get("content-type", "").lower()
            return "image" in content_type or is_image_ext
        
        # 3. Permissive fallback: If blocked (403) but has image extension, trust it
        if response.status_code == 403 and is_image_ext:
            return True
            
        return False
    except Exception:
        # 4. Final fallback: If request fails completely but has image extension, trust it
        return is_image_ext

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
