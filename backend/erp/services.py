from .repository import InvoiceRepository


class InvoiceService:

    @staticmethod
    def list_invoices():

        return InvoiceRepository.list_invoices()