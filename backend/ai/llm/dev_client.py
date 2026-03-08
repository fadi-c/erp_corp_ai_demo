# backend/core/llm/dev_client.py
from .base import BaseLLM

class DevLLM(BaseLLM):

    def ask(self, question: str, context: str) -> str:
        return f"[DEV] Free fake model: '{question[:50]}...' context '{context[:50]}...'"