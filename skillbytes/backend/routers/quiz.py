from fastapi import APIRouter, HTTPException
from database.connection import quiz_sessions_col, questions_col, analytics_col, users_col
from models.schemas import QuizSessionCreate, QuizAnswer, QuizSessionComplete
from utils.helpers import serialize_doc, serialize_list
from bson import ObjectId
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.post("/start")
async def start_quiz(session_data: QuizSessionCreate):
    # Get questions for chapter
    questions = await questions_col.find({
        "chapter_id": session_data.chapter_id
    }).to_list(100)
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this chapter")
    
    random.shuffle(questions)
    question_ids = [str(q["_id"]) for q in questions]
    
    session = {
        "user_id": session_data.user_id,
        "exam_id": session_data.exam_id,
        "subject_id": session_data.subject_id,
        "chapter_id": session_data.chapter_id,
        "started_at": datetime.utcnow(),
        "completed_at": None,
        "status": "in_progress",
        "question_ids": question_ids,
        "current_question_index": 0,
        "answers": [],
        "score": None,
        "total_questions": len(question_ids)
    }
    
    result = await quiz_sessions_col.insert_one(session)
    
    # Log analytics event
    await analytics_col.insert_one({
        "event": "quiz_started",
        "user_id": session_data.user_id,
        "exam_id": session_data.exam_id,
        "subject_id": session_data.subject_id,
        "chapter_id": session_data.chapter_id,
        "session_id": str(result.inserted_id),
        "timestamp": datetime.utcnow(),
        "hour": datetime.utcnow().hour,
        "date": datetime.utcnow().date().isoformat()
    })
    
    created = await quiz_sessions_col.find_one({"_id": result.inserted_id})
    return serialize_doc(created)

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    session = await quiz_sessions_col.find_one({"_id": ObjectId(session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return serialize_doc(session)

@router.get("/session/{session_id}/question")
async def get_current_question(session_id: str):
    session = await quiz_sessions_col.find_one({"_id": ObjectId(session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session["status"] == "completed":
        return {"status": "completed", "session": serialize_doc(session)}
    
    idx = session["current_question_index"]
    question_ids = session["question_ids"]
    
    if idx >= len(question_ids):
        return {"status": "completed", "session": serialize_doc(session)}
    
    q_id = question_ids[idx]
    question = await questions_col.find_one({"_id": ObjectId(q_id)})
    
    return {
        "status": "in_progress",
        "question": serialize_doc(question),
        "question_number": idx + 1,
        "total_questions": len(question_ids),
        "shown_at": datetime.utcnow().isoformat()
    }

@router.post("/answer")
async def submit_answer(answer: QuizAnswer):
    session = await quiz_sessions_col.find_one({"_id": ObjectId(answer.session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session["status"] == "completed":
        raise HTTPException(status_code=400, detail="Session already completed")
    
    # Get question to check correctness
    question = await questions_col.find_one({"_id": ObjectId(answer.question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    is_correct = question["correct_option_id"] == answer.selected_option_id
    response_duration = (answer.answer_submitted_at - answer.question_shown_at).total_seconds()
    
    answer_record = {
        "question_id": answer.question_id,
        "selected_option_id": answer.selected_option_id,
        "correct_option_id": question["correct_option_id"],
        "is_correct": is_correct,
        "question_shown_at": answer.question_shown_at,
        "answer_submitted_at": answer.answer_submitted_at,
        "response_duration_seconds": response_duration
    }
    
    new_index = session["current_question_index"] + 1
    
    await quiz_sessions_col.update_one(
        {"_id": ObjectId(answer.session_id)},
        {
            "$push": {"answers": answer_record},
            "$set": {"current_question_index": new_index}
        }
    )
    
    # Log analytics
    await analytics_col.insert_one({
        "event": "question_answered",
        "user_id": session["user_id"],
        "session_id": answer.session_id,
        "question_id": answer.question_id,
        "is_correct": is_correct,
        "response_duration_seconds": response_duration,
        "timestamp": datetime.utcnow(),
        "hour": datetime.utcnow().hour,
        "date": datetime.utcnow().date().isoformat()
    })
    
    return {
        "is_correct": is_correct,
        "correct_option_id": question["correct_option_id"],
        "explanation": question.get("explanation", ""),
        "response_duration_seconds": response_duration,
        "next_question_index": new_index,
        "total_questions": session["total_questions"]
    }

@router.post("/complete")
async def complete_quiz(data: QuizSessionComplete):
    session = await quiz_sessions_col.find_one({"_id": ObjectId(data.session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    answers = session.get("answers", [])
    total = session["total_questions"]
    correct = sum(1 for a in answers if a.get("is_correct"))
    score = (correct / total * 100) if total > 0 else 0
    
    avg_response_time = 0
    if answers:
        durations = [a.get("response_duration_seconds", 0) for a in answers]
        avg_response_time = sum(durations) / len(durations)
    
    await quiz_sessions_col.update_one(
        {"_id": ObjectId(data.session_id)},
        {"$set": {
            "status": "completed",
            "completed_at": data.completed_at,
            "score": score,
            "correct_answers": correct,
            "avg_response_time": avg_response_time
        }}
    )
    
    # Log completion analytics
    await analytics_col.insert_one({
        "event": "quiz_completed",
        "user_id": session["user_id"],
        "session_id": data.session_id,
        "score": score,
        "correct_answers": correct,
        "total_questions": total,
        "avg_response_time": avg_response_time,
        "timestamp": datetime.utcnow(),
        "date": datetime.utcnow().date().isoformat()
    })
    
    return {
        "session_id": data.session_id,
        "score": score,
        "correct_answers": correct,
        "total_questions": total,
        "avg_response_time": avg_response_time,
        "status": "completed"
    }

@router.get("/history/{user_id}")
async def get_user_history(user_id: str):
    sessions = await quiz_sessions_col.find(
        {"user_id": user_id}
    ).sort("started_at", -1).to_list(50)
    return serialize_list(sessions)

@router.post("/abandon/{session_id}")
async def abandon_quiz(session_id: str, user_id: str):
    session = await quiz_sessions_col.find_one({"_id": ObjectId(session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    await quiz_sessions_col.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"status": "abandoned", "abandoned_at": datetime.utcnow()}}
    )
    
    await analytics_col.insert_one({
        "event": "quiz_abandoned",
        "user_id": user_id,
        "session_id": session_id,
        "questions_answered": session["current_question_index"],
        "total_questions": session["total_questions"],
        "timestamp": datetime.utcnow(),
        "date": datetime.utcnow().date().isoformat()
    })
    
    return {"status": "abandoned"}
