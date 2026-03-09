import os
import json
import logging
import litellm

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, api_key: str = None, provider: str = "groq"):
        self.provider = provider
        if provider == "groq":
            self.model_name = os.getenv("GROQ_MODEL", "groq/llama-3.3-70b-versatile")
            self.api_key = api_key or os.getenv("GROQ_API_KEY")
        else:
            self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
            self.api_key = api_key or os.getenv("GOOGLE_API_KEY")

    def _call_llm(self, prompt: str) -> str:
        try:
            response = litellm.completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                api_key=self.api_key,
                response_format={ "type": "json_object" } if self.provider == "groq" else None
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM Call failed: {e}")
            raise e

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
        Example: {{"Institution Name": "...", "Website": "...", "Logo Url": "...", "Country": "..."}}
        """
        content = self._call_llm(prompt)
        
        try:
            json_str = content.strip('`').replace('json\n', '').strip()
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse JSON: {content}")
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
        5. Generate the SHORTEST POSSIBLE readable URL slug for the institution name. Prefer well-known abbreviations or acronyms (e.g., "diu" for "Daffodil International University", "mit" for "Massachusetts Institute of Technology", "rmu" for "Rabindra Maitree University"). Do not include the country in this slug.
        
        Return in JSON format ONLY:
        {{
            "is_real": boolean,
            "official_website": "string",
            "official_logo_url": "string",
            "country_code": "string",
            "slug": "string",
            "verification_notes": "string"
        }}
        """
        content = self._call_llm(prompt)
        
        try:
            json_str = content.strip('`').replace('json\n', '').strip()
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse JSON: {content}")
            raise e
