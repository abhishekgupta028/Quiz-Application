from fastapi import APIRouter, HTTPException
from database.connection import exams_col
from models.schemas import ExamCreate
from utils.helpers import serialize_doc, serialize_list
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_exams():
    exams = await exams_col.find().to_list(100)
    return serialize_list(exams)

@router.get("/{exam_id}")
async def get_exam(exam_id: str):
    exam = await exams_col.find_one({"_id": ObjectId(exam_id)})
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return serialize_doc(exam)

@router.post("/")
async def create_exam(exam: ExamCreate):
    doc = exam.dict()
    doc["created_at"] = datetime.utcnow()
    result = await exams_col.insert_one(doc)
    created = await exams_col.find_one({"_id": result.inserted_id})
    return serialize_doc(created)
