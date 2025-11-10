from agents import Agent, function_tool
from openai import AsyncOpenAI
import os

# ============================================
# Search Agent for AI Policy Research Assistant
# ============================================
@function_tool
async def perform_search(query: str, reason: str = "") -> dict:
    """Perform a factual web-based search for policy-related queries."""
    try:
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = (
            "You are a Search Agent specializing in finding policy-related data. "
            "Given a research query, return relevant summaries and sources for policy analysis.\n\n"
            f"Task: Search online or from your knowledge for information related to: '{query}'.\n"
            f"Reason for search: {reason}\n\n"
            f"Return your results in JSON with keys: 'title', 'summary', 'source'."
        )

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a policy research assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3
        )

        text = response.choices[0].message.content.strip()
        if not text:
            return {"status": "empty", "results": []}

        return {"status": "ok", "results": [text]}

    except Exception as e:
        return {"status": "error", "message": str(e)}



