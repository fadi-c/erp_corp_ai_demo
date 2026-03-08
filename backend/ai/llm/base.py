from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Interface pour LLM service, dev <-> prod."""

    @abstractmethod
    def ask(self, question: str, context: str) -> str:
        pass