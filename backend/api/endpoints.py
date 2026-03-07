from ninja import Router
from .schemas import QuestionRequest, QuestionResponse

router = Router()


@router.get("/health")
def health(request):
    return {"status": "ok"}


@router.post("/question", response=QuestionResponse)
def ask_question(request, payload: QuestionRequest):
    return QuestionResponse(
        answer="AI analysis placeholder",
        sources=[]
    )