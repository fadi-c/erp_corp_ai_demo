# backend/core/llm/factory.py
import os
from django.conf import settings
from .openai_client import OpenAILLM
from .dev_client import DevLLM
from .base import BaseLLM
class LLMFactory:

    @staticmethod
    def get_llm() -> BaseLLM:
        llm_env = getattr(settings, "AI_LLM", "FAKE").upper()

        if llm_env == "OPENAI":
            return OpenAILLM()
        else:
            return DevLLM()