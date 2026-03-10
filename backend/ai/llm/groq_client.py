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
You are a professional AI analyst specialized in ERP and financial data.

Context:
{context}

Question:
{question}

Analyze the data carefully and provide a clear, concise, and actionable explanation suitable for business decisions. 
"""

        response = client.chat.completions.create(
            model=self.MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
    