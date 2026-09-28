from fastapi import FastAPI

from app.routes import router


app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="AI-powered comic story creator",
    version="1.0.0"
)

app.include_router(router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "application": "ComicCraft"
    }
