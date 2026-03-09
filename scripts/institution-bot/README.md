# Institution Bot - Local Testing Guide

This guide explains how to run the Institution Bot locally to test its verification logic using the Google Agent Development Kit (ADK) and Gemini.

## Prerequisites

1. **Python 3.10+**
2. **Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/).
3. **GitHub Personal Access Token**: Create a token with `repo` scope at [GitHub Settings](https://github.com/settings/tokens).

## Setup Instructions

1. **Navigate to the bot directory**:
   ```bash
   cd scripts/institution-bot
   ```

2. **Create and Activate a Virtual Environment (Recommended)**:
   This ensures your project dependencies don't interfere with your system Python.
   
   **Using venv (Built-in):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   
   **Using pyenv (If installed):**
   ```bash
   pyenv local 3.10.0  # Or any 3.10+ version
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in `scripts/institution-bot/` with the following content:
   ```text
   GOOGLE_API_KEY=your_gemini_api_key
   GITHUB_TOKEN=your_github_pat
   GITHUB_REPOSITORY=lightoj-dev/bugs-and-features
   ISSUE_NUMBER=251
   ```

## Running the Agent

You can run the agent in two ways:

### 1. Standard Execution (Script Mode)
Run the main entry point. This will trigger the agent to analyze the issue specified in your `.env` file.
```bash
python main.py
```

### 2. Interactive/Debug Mode (ADK Web UI)
The ADK provides a powerful Web UI to see the agent's "Thought Signatures" (how it uses Google Search and Tools).
```bash
adk web
```
Then open `http://localhost:8000` in your browser.

## What to Expect
- The agent will call `get_issue_content` to read issue #251.
- It will use **Google Search** to verify the institution "Daffodil International University" (or whichever is in the issue).
- It will attempt to find the official logo and website.
- Because it is in **Local Test Mode**, it will print `[Local Test]` messages instead of actually creating anything on LightOJ.
- The final output in your terminal will contain the agent's full verification report.
