from ai.retrieval import RetrievalService


class RagPipeline:

    @staticmethod
    def build_context(question: str):

        results = RetrievalService.search(question)

        context_parts = []

        for item in results:

            invoice = item.invoice

            context_parts.append(
                f"""
                Invoice {invoice.id}
                Description: {invoice.description}
                Amount: {invoice.amount}
                Margin: {invoice.margin}
                Date: {invoice.date}
                """
            )

        context = "\n".join(context_parts)

        return context, results