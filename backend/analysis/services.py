from ai.rag_pipeline import RagPipeline
from ai.llm.factory import LLMFactory

class AnalysisService:
    @staticmethod
    def answer_question(question: str):
        context, results = RagPipeline.build_context(question)
        answer = LLMFactory.get_llm().ask(question, context)
        sources = [item.invoice.id for item in results]
        return answer, sources