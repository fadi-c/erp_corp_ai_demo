import os
from openai import OpenAI
from .base import BaseLLM

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


class GroqLLM(BaseLLM):

    MODEL = "openai/gpt-oss-20b"

    def ask(self, question: str, context: str) -> str:
        prompt = f"""
You are an AI analyst helping understand ERP financial data.

Context:
{context}

Question:
{question}

Provide a concise explanation.
"""

        response = client.chat.completions.create(
            model=self.MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
    