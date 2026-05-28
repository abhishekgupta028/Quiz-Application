from fastapi import APIRouter, HTTPException
from database.connection import questions_col
from models.schemas import QuestionCreate
from utils.helpers import serialize_doc, serialize_list
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_questions(chapter_id: str = None, subject_id: str = None, exam_id: str = None):
    query = {}
    if chapter_id:
        query["chapter_id"] = chapter_id
    if subject_id:
        query["subject_id"] = subject_id
    if exam_id:
        query["exam_id"] = exam_id
    questions = await questions_col.find(query).to_list(500)
    return serialize_list(questions)

@router.get("/{question_id}")
async def get_question(question_id: str):
    question = await questions_col.find_one({"_id": ObjectId(question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return serialize_doc(question)

@router.post("/")
async def create_question(question: QuestionCreate):
    doc = question.dict()
    doc["created_at"] = datetime.utcnow()
    result = await questions_col.insert_one(doc)
    created = await questions_col.find_one({"_id": result.inserted_id})
    return serialize_doc(created)
