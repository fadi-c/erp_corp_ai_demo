from ninja import Router
from .schemas import QuestionRequest, QuestionResponse
from erp.services import InvoiceService
from erp.models import Invoice
from .schemas import InvoiceSchema
from analysis.services import AnalysisService

router = Router()


@router.get("/health")
def health(request):
    return {"status": "ok"}


@router.post("/question", response=QuestionResponse)
def ask_question(request, payload: QuestionRequest):

    answer, sources = AnalysisService.answer_question(
        payload.question
    )

    return QuestionResponse(
        answer=answer,
        sources=sources
    )

@router.get("/invoices", response=list[InvoiceSchema])
def list_invoices(request):

    invoices = InvoiceService.list_invoices()

    return invoices