import requests
import json
import logging
import os

logger = logging.getLogger(__name__)

class LightOJAPIClient:
    def __init__(self, api_base_url: str, handle: str = None, password: str = None):
        self.api_base_url = api_base_url
        self.handle = handle
        self.password = password
        self.token = None
        self.session = requests.Session()
        
        # Default headers based on your curl
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "origin": "https://lightoj.com",
            "referer": "https://lightoj.com/auth/login"
        }

    def login(self):
        """
        Authenticates with LightOJ and retrieves the session token.
        """
        if not self.handle or not self.password:
            logger.error("LightOJ handle or password missing.")
            return False

        recaptcha_token = os.getenv("LIGHTOJ_RECAPTCHA_TOKEN")
        if not recaptcha_token:
            logger.error("LIGHTOJ_RECAPTCHA_TOKEN missing.")
            return False
        login_url = f"{self.api_base_url}/v1/auth/login"
        payload = {
            "handleOrEmail": self.handle,
            "password": self.password,
            "emailVerified": True,
            "recaptchaToken": recaptcha_token
        }

        try:
            logger.info(f"Attempting login for {self.handle}...")
            response = self.session.post(login_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                # Assuming the token is in the response data
                # Adjust based on real API response structure
                self.token = data.get("token") or data.get("accessToken")
                if self.token:
                    self.headers["Authorization"] = f"Bearer {self.token}"
                
                logger.info("Login successful.")
                return True
            else:
                logger.error(f"Login failed ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            logger.exception(f"Error during login: {e}")
            return False

    def search_institution(self, name: str):
        """
        Searches if the institution already exists in the admin list.
        """
        url = f"{self.api_base_url}/v1/admin/institutions/?page=1&perPage=100"
        try:
            logger.info(f"Fetching institution list to search for '{name}'...")
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                # The data structure might vary, usually it's a list under 'data' or 'institutions'
                # Let's assume standard pagination structure
                institutions = data.get("data", [])
                if not isinstance(institutions, list):
                    # Fallback if the whole response is the list
                    institutions = data if isinstance(data, list) else []

                for inst in institutions:
                    if inst.get("name", "").lower() == name.lower():
                        logger.info(f"Found existing institution: {name}")
                        return inst
                
                return None
            else:
                logger.error(f"Failed to fetch institutions ({response.status_code}): {response.text}")
                return None
        except Exception as e:
            logger.exception(f"Error searching institution: {e}")
            return None

    def create_institution(self, name: str, website: str, logo_url: str, country_code: str):
        """
        Creates a new institution on LightOJ using the verified admin payload.
        """
        url = f"{self.api_base_url}/v1/admin/institutions/"
        
        # Simple handle generator: lowercase, no spaces, limited length
        handle = name.lower().replace(" ", "-")[:20]
        
        payload = {
            "institutionId": "",
            "institutionNameStr": name,
            "institutionHandleStr": handle,
            "institutionWebsiteStr": website,
            "isHiddenBool": False,
            "institutionLogoLinkStr": logo_url,
            "institutionCountryCodeStr": country_code # e.g., "BD"
        }
        
        try:
            logger.info(f"Creating institution: {name} with handle {handle}...")
            response = self.session.post(url, headers=self.headers, json=payload)
            if response.status_code in [200, 201]:
                logger.info(f"Successfully created institution: {name}")
                return {"status": "success", "data": response.json()}
            else:
                logger.error(f"Failed to create institution ({response.status_code}): {response.text}")
                return {"status": "error", "message": response.text}
        except Exception as e:
            logger.exception(f"Error creating institution: {e}")
            return {"status": "error", "message": str(e)}
