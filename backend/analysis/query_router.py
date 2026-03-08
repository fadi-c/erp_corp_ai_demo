import re


class QueryRouter:

    SQL_PATTERNS = [
        r"how many",
        r"count",
        r"per month",
        r"per year",
        r"average",
        r"sum",
        r"total"
    ]

    @staticmethod
    def route(question: str):

        q = question.lower()

        for pattern in QueryRouter.SQL_PATTERNS:
            if re.search(pattern, q):
                return "sql"

        if len(question.split()) <= 3:
            return "keyword"

        return "vector"