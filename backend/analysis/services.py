from ai.llm.factory import LLMFactory
from analysis.hybrid_retrieval import HybridRetrieval
from erp.models import Invoice

class AnalysisService:

    @staticmethod
    def answer_question(question: str):
        route, results, context = HybridRetrieval.retrieve(question)

        if route == "sql":
            sql_context = "\n".join([f"{r['month'].strftime('%Y-%m')}: {r['count']} invoices" for r in results])
            answer = LLMFactory.get_llm().ask(question, sql_context)

            months = [r['month'].month for r in results]
            invoice_ids = list(
                Invoice.objects.filter(date__month__in=months).values_list('id', flat=True)
            )

            return answer, invoice_ids


        if route == "keyword":
            keyword_context = "\n".join([f"Invoice {i.id}: {i.description}" for i in results])
            answer = LLMFactory.get_llm().ask(question, keyword_context)
            return answer, [i.id for i in results]

        # vector
        llm_answer = LLMFactory.get_llm().ask(question, context)
        sources = [item.invoice.id for item in results]
        return llm_answer, sources