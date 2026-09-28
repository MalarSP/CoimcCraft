from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from app.ai.gemini_flash import generate_story, generate_image

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate")
async def generate_comic(
    request: Request,
    topic: str = Form(...)
):
    story = generate_story(topic)
    image = generate_image(topic)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "story": story,
            "image": image,
            "topic": topic
        }
    )


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "application": "ComicCraft"
    }