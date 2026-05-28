from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import exams, subjects, chapters, questions, quiz, analytics, seed
import uvicorn

app = FastAPI(title="SkillBytes API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(exams.router, prefix="/api/exams", tags=["Exams"])
app.include_router(subjects.router, prefix="/api/subjects", tags=["Subjects"])
app.include_router(chapters.router, prefix="/api/chapters", tags=["Chapters"])
app.include_router(questions.router, prefix="/api/questions", tags=["Questions"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(seed.router, prefix="/api/seed", tags=["Seed"])

@app.get("/")
def root():
    return {"message": "SkillBytes API is running", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
