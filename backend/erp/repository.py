from .models import Invoice


class InvoiceRepository:

    @staticmethod
    def list_invoices():
        return Invoice.objects.all().order_by("-date")


    @staticmethod
    def get_invoice(invoice_id: int):

        return Invoice.objects.get(id=invoice_id)


    @staticmethod
    def create_invoice(**data):

        return Invoice.objects.create(**data)