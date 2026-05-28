from fastapi import APIRouter, HTTPException
from database.connection import subjects_col
from models.schemas import SubjectCreate
from utils.helpers import serialize_doc, serialize_list
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_subjects(exam_id: str = None):
    query = {}
    if exam_id:
        query["exam_id"] = exam_id
    subjects = await subjects_col.find(query).to_list(100)
    return serialize_list(subjects)

@router.get("/{subject_id}")
async def get_subject(subject_id: str):
    subject = await subjects_col.find_one({"_id": ObjectId(subject_id)})
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return serialize_doc(subject)

@router.post("/")
async def create_subject(subject: SubjectCreate):
    doc = subject.dict()
    doc["created_at"] = datetime.utcnow()
    result = await subjects_col.insert_one(doc)
    created = await subjects_col.find_one({"_id": result.inserted_id})
    return serialize_doc(created)
