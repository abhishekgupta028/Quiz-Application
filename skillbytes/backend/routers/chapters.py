from fastapi import APIRouter, HTTPException
from database.connection import chapters_col
from models.schemas import ChapterCreate
from utils.helpers import serialize_doc, serialize_list
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_chapters(subject_id: str = None, exam_id: str = None):
    query = {}
    if subject_id:
        query["subject_id"] = subject_id
    if exam_id:
        query["exam_id"] = exam_id
    chapters = await chapters_col.find(query).sort("order", 1).to_list(100)
    return serialize_list(chapters)

@router.get("/{chapter_id}")
async def get_chapter(chapter_id: str):
    chapter = await chapters_col.find_one({"_id": ObjectId(chapter_id)})
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return serialize_doc(chapter)

@router.post("/")
async def create_chapter(chapter: ChapterCreate):
    doc = chapter.dict()
    doc["created_at"] = datetime.utcnow()
    result = await chapters_col.insert_one(doc)
    created = await chapters_col.find_one({"_id": result.inserted_id})
    return serialize_doc(created)
