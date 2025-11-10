import asyncio
from openai import AsyncOpenAI
import os

class Agent:
    """
    Base asynchronous LLM agent for AI Policy Research Assistant.
    Handles OpenAI chat completions with system + user messages.
    """
    def __init__(self, name, instructions, model, tools=None, output_type=None):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools or []
        self.output_type = output_type
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def run(self, prompt):
        print(f"[{self.name}] Running on {self.model}")
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        class Result:
            final_output = response.choices[0].message.content
        return Result()


# -------------------------------
# Compatibility placeholder
# -------------------------------
def function_tool(func):
    """Decorator placeholder for backward compatibility with agents using @function_tool"""
    return func
