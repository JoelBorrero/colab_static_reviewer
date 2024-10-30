from fastapi import APIRouter

from app.gpt.services import solve_task, translate_to_python
from app.models import SolveTaskRequest, TranslateCodeRequest


router = APIRouter(prefix="/gpt")

@router.post("/solve")
async def solve(body: SolveTaskRequest):
    """
    Solve a task
    """
    res = solve_task(body.prompt)
    return res


@router.post("/translate")
async def translate(body: TranslateCodeRequest):
    """
    Translate from Swift to Python
    """
    res = translate_to_python(body.code)
    return res
