from ninja import Router
from .schemas import QuestionRequest, QuestionResponse
from erp.services import InvoiceService
from erp.models import Invoice
from .schemas import InvoiceSchema
from analysis.services import AnalysisService
from observability.metrics import api_requests, api_latency, missing_invoice_embeddings
import time

router = Router()



@router.get("/health")
def health(request):
    start = time.time()
    try:
        return {"status": "ok"}
    finally:
        latency = time.time() - start
        api_requests.labels(endpoint="/health", method="GET", status="200").inc()
        api_latency.labels(endpoint="/health", method="GET").observe(latency)

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