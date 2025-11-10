from pydantic import BaseModel, Field
from agents import Agent

# ============================================
# Fact Checker Agent for AI Policy Research Assistant
# ============================================

INSTRUCTIONS = (
    "You are a fact-checking agent for AI policy research. Given a set of summarized search results, "
    "evaluate the credibility and factual reliability of the content. Only accept verified, authoritative sources "
    "such as EU, OECD, UNESCO, UN, and academic institutions. Identify and exclude misinformation, bias, or speculation."
)

class FactCheckResult(BaseModel):
    valid_sources: list[str] = Field(description="List of sources considered credible and reliable.")
    excluded_sources: list[str] = Field(description="List of sources that were excluded due to low reliability.")
    summary: str = Field(description="Clean summary after fact-checking and filtering.")

fact_checker_agent = Agent(
    name="FactCheckerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=FactCheckResult,
)
