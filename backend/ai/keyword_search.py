from erp.models import Invoice


class KeywordSearch:

    @staticmethod
    def search(question, limit=10):

        return list(
            Invoice.objects.filter(
                description__icontains=question
            )[:limit]
        )