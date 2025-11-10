import json
from agents import Agent, function_tool

@function_tool
def create_search_plan(research_query: str) -> dict:
    """
    Generate a fixed structured search plan for the policy research.
    Always returns a dict with 'searches' list, containing 'query' and 'reason'.
    """
    plan = [
        {"query": f"{research_query} site:europa.eu", "reason": "Find EU policy frameworks"},
        {"query": f"{research_query} site:oecd.org", "reason": "Locate OECD reports and recommendations"},
        {"query": f"{research_query} site:un.org OR site:unesco.org", "reason": "Check UN policy documents"},
        {"query": f"{research_query} site:brookings.edu OR site:rand.org", "reason": "Find think-tank analysis"},
        {"query": f"{research_query} site:mit.edu", "reason": "Review academic and research perspectives"},
    ]
    return {"searches": plan}


INSTRUCTIONS = (
    "You are a planning agent that creates a structured plan for conducting policy research. "
    "Given a research topic, design 3–5 high-quality search queries on reputable domains "
    "such as EU, OECD, UN, RAND, and MIT. "
    "Return the result strictly as JSON with a key 'searches', where each element "
    "includes 'query' and 'reason'."
)

planner_agent = Agent(
    name="PlannerAgentPolicy",
    instructions=INSTRUCTIONS,
    tools=[create_search_plan],
    model="gpt-4o-mini",
)


async def run_planner(query: str):
    """
    Safe async wrapper for PlannerAgent.
    Ensures a valid structure with `final_output.searches`.
    """

    try:
        result = await planner_agent.run(f"Research query: {query}")

        if not hasattr(result, "final_output"):
            class Fallback:
                final_output = create_search_plan(query)
            return Fallback()

        if isinstance(result.final_output, str):
            try:
                parsed = json.loads(result.final_output)
                result.final_output = parsed
            except json.JSONDecodeError:
                result.final_output = create_search_plan(query)

        if not isinstance(result.final_output, dict) or "searches" not in result.final_output:
            result.final_output = create_search_plan(query)

        return result

    except Exception as e:
        print("PlannerAgent error:", e)
        class Fallback:
            final_output = create_search_plan(query)
        return Fallback()
