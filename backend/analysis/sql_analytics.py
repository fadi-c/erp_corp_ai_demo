from django.db.models import Count
from django.db.models.functions import TruncMonth
from erp.models import Invoice


class SQLAnalyticsService:

    @staticmethod
    def invoices_by_month():

        qs = (
            Invoice.objects
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        return list(qs)

    @staticmethod
    def top_customers(limit=5):

        qs = (
            Invoice.objects
            .values("customer__name")
            .annotate(total=Count("id"))
            .order_by("-total")[:limit]
        )

        return list(qs)