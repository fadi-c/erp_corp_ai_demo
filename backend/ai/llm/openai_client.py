# backend/core/llm/openai_client.py
import os
from openai import OpenAI
from .base import BaseLLM

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAILLM(BaseLLM):

    MODEL = "gpt-4o-mini"

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