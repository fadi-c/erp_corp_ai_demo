from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def ask(self, question: str, context: str) -> str:
        pass