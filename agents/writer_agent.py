import os
import json
from pydantic import BaseModel, Field
from agents import Agent
from openai import OpenAI


INSTRUCTIONS = (
    "You are a senior policy analyst tasked with writing a detailed, structured policy brief "
    "based on verified research results. You will receive a query and fact-checked information.\n\n"
    "Your output MUST strictly follow this Pydantic schema:\n"
    "short_summary: str\n"
    "markdown_report: str\n"
    "follow_up_research: list[str]\n\n"
    "Structure the report with the following sections:\n"
    "1. Executive Summary\n"
    "2. Key Policy Challenges\n"
    "3. International Practices\n"
    "4. Recommendations\n"
    "5. References\n\n"
    "Use Markdown formatting (## headings, **bold**, bullet points). "
    "Do NOT wrap JSON in code blocks. Return valid JSON only."
)

class PolicyReportData(BaseModel):
    short_summary: str
    markdown_report: str
    follow_up_research: list[str]

writer_agent = Agent(
    name="WriterAgentPolicy",
    instructions=INSTRUCTIONS,
    model="gpt-4o",
    output_type=PolicyReportData,
)

def generate_report(query: str, facts: str):
    """Generates structured policy report JSON"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    full_prompt = f"Query: {query}\nFacts: {facts}"

    response = client.chat.completions.create(
        model=writer_agent.model,
        messages=[
            {"role": "system", "content": writer_agent.instructions},
            {"role": "user", "content": full_prompt},
        ]
    )

    content = response.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("WriterAgent returned invalid JSON, fallback to text.")
        return {
            "short_summary": "Summary unavailable.",
            "markdown_report": content,
            "follow_up_research": [],
        }
