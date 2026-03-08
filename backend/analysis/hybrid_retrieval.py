from ai.keyword_search import KeywordSearch
from analysis.sql_analytics import SQLAnalyticsService
from analysis.query_router import QueryRouter
from ai.rag_pipeline import RagPipeline
class HybridRetrieval:

    @staticmethod
    def retrieve(question: str):
        route = QueryRouter.route(question)

        if route == "sql":
            return "sql", SQLAnalyticsService.invoices_by_month(), None

        if route == "keyword":
            return "keyword", KeywordSearch.search(question), None

        # vector
        context, results = RagPipeline.build_context(question)
        return "vector", results, context