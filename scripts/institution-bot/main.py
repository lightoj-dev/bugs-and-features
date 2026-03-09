import os
import sys
import json
import logging
import asyncio
from dotenv import load_dotenv
from github_client import GitHubClient
from lightoj_api import LightOJAPIClient
from gemini_client import GeminiClient
from agent import institution_agent
from google.adk.runners import InMemoryRunner
from google.genai import types

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from search_tool import search_institution_details, is_valid_image_url

def run_simple(gemini_client, combined_text, loj_client, gh_client, issue_number):
    """
    Simple execution using Tavily for search and Gemini for analysis.
    """
    logger.info("Using simple Gemini client + Tavily Search...")
    
    # 1. Parse content
    info = gemini_client.analyze_content(combined_text)
    name = info.get("Institution Name")
    website = info.get("Website")
    logo_url = info.get("Logo Url")
    country = info.get("Country")

    if not name:
        gh_client.comment_on_issue(issue_number, "I couldn't find the Institution Name in the request. Please provide it.")
        return

    # 2. Web Search via Tavily
    logger.info(f"Searching online for: {name} in {country}...")
    search_results = search_institution_details(name, country or "")

    # 3. Verify via Gemini
    logger.info(f"Verifying institution details...")
    verification = gemini_client.verify_institution(name, website, country, search_results)
    
    logger.info("--- Verification Results ---")
    logger.info(json.dumps(verification, indent=2))

    if not verification.get("is_real"):
        gh_client.comment_on_issue(issue_number, f"I couldn't verify this institution. Notes: {verification.get('verification_notes')}")
        return

    # Update with found info
    final_web = verification.get("official_website") or website
    final_logo = verification.get("official_logo_url") or logo_url
    final_country_code = verification.get("country_code") or "BD"
    final_slug = verification.get("slug")

    # --- Logo Validation ---
    logger.info(f"Validating logo URL: {final_logo}")
    if not is_valid_image_url(final_logo):
        logger.warning(f"Invalid logo URL detected: {final_logo}")
        gh_client.comment_on_issue(issue_number, f"I verified the institution, but I couldn't find a valid logo URL (the one I found was: `{final_logo}`).\n\nPlease provide a direct link to a valid image logo (PNG/JPG/SVG) to complete the request.")
        return

    # 4. LightOJ Logic
    logger.info(f"Searching LightOJ for '{name}'...")
    existing = loj_client.search_institution(name)
    
    if not existing:
        logger.info(f"Creating on LightOJ: {name}, {final_web}, {final_logo}, {final_country_code}, slug={final_slug}")
        result = loj_client.create_institution(name, final_web, final_logo, final_country_code, slug=final_slug)
        
        if result.get("status") == "success":
            # Determine the handle used (logic same as in lightoj_api.py)
            slug = final_slug or "".join(c if c.isalnum() or c == " " else "" for c in name).lower().replace(" ", "-")
            suffix = f"-{final_country_code.lower()}"
            max_slug_len = 50 - len(suffix)
            handle = f"{slug[:max_slug_len].strip('-')}{suffix}"
            
            institution_url = f"https://lightoj.com/institutions/{handle}"

            # Post success
            gh_client.comment_on_issue(issue_number, f"Verified and Created!\n- Name: {name}\n- Website: {final_web}\n- Logo: {final_logo}\n- Country Code: {final_country_code}\n- LightOJ Link: {institution_url}")
            gh_client.close_issue(issue_number)
        else:
            error_msg = result.get("message", "")
            if "unique constraint" in error_msg and "institutionhandlestr_unique" in error_msg:
                gh_client.comment_on_issue(issue_number, f"I verified the institution, but a handle for '{name}' already exists. An admin might need to link it manually.")
            else:
                gh_client.comment_on_issue(issue_number, f"Verification successful, but I encountered an error during creation: {error_msg}")
    else:
        gh_client.comment_on_issue(issue_number, f"'{name}' already exists in our system. Closing.")
        gh_client.close_issue(issue_number)

async def run_with_adk(issue_number):
    """
    Runs using the professional ADK agent with configured retry logic.
    """
    runner = InMemoryRunner(agent=institution_agent)
    user_id = "bot_user"
    session_id = f"issue_{issue_number}"
    
    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    user_prompt = types.Content(
        role="user",
        parts=[types.Part(text=f"Please process the institution add request in issue #{issue_number}. Use your tools to gather all necessary info from the issue body and comments.")]
    )
    
    logger.info("Executing ADK Agent...")
    final_resp = ""
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=user_prompt):
        if hasattr(event, 'content') and event.content:
            if event.is_final_response():
                final_resp = event.content.parts[0].text
                logger.info(f"FINAL RESPONSE:\n{final_resp}")
            elif hasattr(event, 'is_thought') and event.is_thought():
                logger.info(f"AGENT THOUGHT: {event.content.parts[0].text}")
            elif hasattr(event, 'is_call') and event.is_call():
                logger.info(f"TOOL CALL: {event.content.parts[0].text}")
    return final_resp

async def main():
    load_dotenv()
    
    # Required environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    gemini_api_key = os.getenv("GOOGLE_API_KEY")
    issue_number = os.getenv("ISSUE_NUMBER")

    if not all([github_token, gemini_api_key, issue_number]):
        logger.error("Missing credentials or ISSUE_NUMBER.")
        sys.exit(1)

    gh_client = GitHubClient(github_token)
    loj_client = LightOJAPIClient(
        "https://lightoj.com/api", 
        os.getenv("LIGHTOJ_HANDLE"), 
        os.getenv("LIGHTOJ_PASSWORD")
    )
    gemini_client = GeminiClient(gemini_api_key)

    try:
        # 0. Login to LightOJ
        if not loj_client.login():
            logger.error("Could not login to LightOJ. Aborting.")
            return

        # Use Simple Client by default for Free Tier compatibility
        issue = gh_client.get_issue(int(issue_number))
        comments = issue.get_comments()
        combined_text = f"ISSUE_BODY:\n{issue.body}\n\nCOMMENTS:\n"
        for comment in comments:
            combined_text += f"USER {comment.user.login}: {comment.body}\n"

        logger.info(f"Running simple mode for issue #{issue_number}")
        run_simple(gemini_client, combined_text, loj_client, gh_client, int(issue_number))

    except Exception as e:
        logger.exception(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
