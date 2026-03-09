import os
import json
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-flash-latest"

    def analyze_content(self, text: str) -> dict:
        """
        Parses issue content to extract institution details.
        """
        prompt = f"""
        Extract the following information from the text:
        1. Institution Name
        2. Website
        3. Logo Url
        4. Country

        Text:
        {text}

        Return the result in JSON format ONLY.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        
        try:
            json_str = response.text.strip('`').replace('json\n', '').strip()
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse JSON: {response.text}")
            raise e

    def verify_institution(self, name: str, website: str, country: str, search_results: str) -> dict:
        """
        Verifies the institution using provided web search results.
        """
        prompt = f"""
        You are an expert verifier. Based on the provided SEARCH RESULTS, verify if this institution is real.
        
        Institution to Verify:
        Name: {name}
        Proposed Website: {website}
        Country: {country}

        {search_results}

        Instructions:
        1. Determine if the institution exists and is active.
        2. Find the correct official website if the proposed one is wrong or missing.
        3. Find a direct URL to an official logo image. Check the 'FOUND IMAGE URLS' section carefully for the best candidate. It should be a direct link to an image file (PNG, JPG, SVG).
        4. CRITICAL: Identify the ISO 3166-1 alpha-2 country code (e.g., "BD" for Bangladesh, "IN" for India, "US" for USA).
        
        Return in JSON format ONLY:
        {{
            "is_real": boolean,
            "official_website": "string",
            "official_logo_url": "string",
            "country_code": "string",
            "verification_notes": "string"
        }}
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        
        try:
            json_str = response.text.strip('`').replace('json\n', '').strip()
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse JSON: {response.text}")
            raise e
