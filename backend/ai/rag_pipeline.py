from ai.retrieval import RetrievalService


class RagPipeline:

    @staticmethod
    def build_context(question: str):

        results = RetrievalService.search(question)

        context_parts = []

        for item in results:
            invoice = item.invoice
            customer = invoice.customer
            orders = invoice.order_set.all() 
            orders_str = "\n".join([
                f"- {o.product.name} ({o.product.category}): {o.quantity} units @ {o.price} EUR"
                for o in orders
            ]) or "No orders linked"

            context_parts.append(
                f"""
Invoice ID: {invoice.id}
Customer: {customer.name} ({customer.industry})
Description: {invoice.description}
Financial data:
- Amount: {invoice.amount} EUR
- Margin: {invoice.margin} EUR
Invoice date: {invoice.date}
Orders:
{orders_str}
"""
            )

        context = "\n".join(context_parts)
        return context, results