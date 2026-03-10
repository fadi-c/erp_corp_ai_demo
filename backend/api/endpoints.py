from ninja import Router
from .schemas import QuestionRequest, QuestionResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from erp.services import InvoiceService
from erp.models import Invoice
from .schemas import InvoiceSchema
from analysis.services import AnalysisService
from observability.metrics import api_requests, api_latency
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

@router.get("/invoices", response=dict)
def list_invoices(request, page: int = 1, page_size: int = 10):
    invoices_qs = InvoiceService.list_invoices()

    paginator = Paginator(invoices_qs, page_size)
    try:
        invoices_page = paginator.page(page)
    except PageNotAnInteger:
        invoices_page = paginator.page(1)
    except EmptyPage:
        invoices_page = []

    results = [InvoiceSchema.from_orm(inv).dict() for inv in invoices_page] if invoices_page else []

    return {
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "current_page": page,
        "results": results
    }