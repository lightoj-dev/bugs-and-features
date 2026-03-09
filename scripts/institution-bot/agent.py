from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.models.google_llm import Gemini
from google.genai import types
from tools import get_issue_content, post_comment_to_issue, close_issue, search_lightoj_institution, create_lightoj_institution

# Define the Institution Bot Agent with Retry Logic for 429 errors
institution_agent = LlmAgent(
    name="InstitutionBot",
    model=Gemini(
        model="gemini-flash-latest", # Switching to 1.5-flash which might have more quota
        retry_options=types.HttpRetryOptions(
            initial_delay=10.0, # Wait 10 seconds before first retry
            attempts=3          # Try 3 times total
        )
    ),
    instruction="""
    You are an automated assistant for LightOJ. Your task is to process institution add requests from GitHub issues.
    
    Workflow:
    1. Retrieve the content of the issue (body and comments) using `get_issue_content`.
    2. Extract details: Institution Name, Website, Logo URL, and Country.
    3. Use Google Search to verify if the institution is real and active.
    4. If the logo URL is missing or incorrect, find the official logo URL using Google Search.
    5. REPORT YOUR FINDINGS clearly in the final output (Verification status, Official Website found, Official Logo URL found).
    6. Check if the institution already exists on LightOJ using `search_lightoj_institution`.
    7. If it exists, inform the user via a comment using `post_comment_to_issue` and close the issue using `close_issue`.
    8. If it doesn't exist and is verified as real, create it using `create_lightoj_institution`.
    9. Post a success message on the issue and close it.
    
    FOR LOCAL TESTING: Be very detailed about what you found online in your final response.
    """,
    tools=[
        google_search,
        get_issue_content,
        post_comment_to_issue,
        close_issue,
        search_lightoj_institution,
        create_lightoj_institution
    ]
)
