from fastapi import APIRouter
from database.connection import analytics_col, quiz_sessions_col, users_col
from utils.helpers import serialize_doc, serialize_list
from datetime import datetime, timedelta
from collections import defaultdict

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    """Returns all analytics in one call for dashboard"""
    now = datetime.utcnow()
    today = now.date().isoformat()
    week_ago = (now - timedelta(days=7)).isoformat()
    
    # Daily active users
    dau_pipeline = [
        {"$match": {"date": today}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "count"}
    ]
    dau_result = await analytics_col.aggregate(dau_pipeline).to_list(1)
    dau = dau_result[0]["count"] if dau_result else 0

    # Weekly active users
    wau_pipeline = [
        {"$match": {"timestamp": {"$gte": now - timedelta(days=7)}}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "count"}
    ]
    wau_result = await analytics_col.aggregate(wau_pipeline).to_list(1)
    wau = wau_result[0]["count"] if wau_result else 0

    # Questions served (shown)
    questions_served = await analytics_col.count_documents({"event": "question_answered"})

    # Questions answered
    questions_answered = await analytics_col.count_documents({"event": "question_answered"})

    # Average response time
    avg_rt_pipeline = [
        {"$match": {"event": "question_answered"}},
        {"$group": {"_id": None, "avg_rt": {"$avg": "$response_duration_seconds"}}}
    ]
    avg_rt_result = await analytics_col.aggregate(avg_rt_pipeline).to_list(1)
    avg_response_time = round(avg_rt_result[0]["avg_rt"], 2) if avg_rt_result and avg_rt_result[0]["avg_rt"] else 0

    # Quiz completion rate
    total_started = await analytics_col.count_documents({"event": "quiz_started"})
    total_completed = await analytics_col.count_documents({"event": "quiz_completed"})
    completion_rate = round((total_completed / total_started * 100), 1) if total_started > 0 else 0

    # Peak activity hours
    peak_pipeline = [
        {"$group": {"_id": "$hour", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    peak_result = await analytics_col.aggregate(peak_pipeline).to_list(24)
    peak_hours = [{"hour": r["_id"], "count": r["count"]} for r in peak_result if r["_id"] is not None]

    # Drop-off analysis
    dropoff_pipeline = [
        {"$match": {"event": {"$in": ["quiz_started", "quiz_completed", "quiz_abandoned"]}}},
        {"$group": {"_id": "$event", "count": {"$sum": 1}}}
    ]
    dropoff_result = await analytics_col.aggregate(dropoff_pipeline).to_list(10)
    dropoff = {r["_id"]: r["count"] for r in dropoff_result}

    # Avg questions per session
    avg_q_pipeline = [
        {"$match": {"event": "quiz_completed"}},
        {"$group": {"_id": None, "avg_q": {"$avg": "$total_questions"}}}
    ]
    avg_q_result = await analytics_col.aggregate(avg_q_pipeline).to_list(1)
    avg_questions_per_session = round(avg_q_result[0]["avg_q"], 1) if avg_q_result and avg_q_result[0]["avg_q"] else 0

    # Daily quiz activity (last 14 days)
    daily_pipeline = [
        {"$match": {
            "event": "quiz_started",
            "timestamp": {"$gte": now - timedelta(days=14)}
        }},
        {"$group": {"_id": "$date", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    daily_result = await analytics_col.aggregate(daily_pipeline).to_list(14)
    daily_activity = [{"date": r["_id"], "quizzes": r["count"]} for r in daily_result]

    # Score distribution
    score_pipeline = [
        {"$match": {"event": "quiz_completed", "score": {"$exists": True}}},
        {"$bucket": {
            "groupBy": "$score",
            "boundaries": [0, 20, 40, 60, 80, 101],
            "default": "Other",
            "output": {"count": {"$sum": 1}}
        }}
    ]
    score_result = await analytics_col.aggregate(score_pipeline).to_list(10)
    score_distribution = [
        {"range": "0-20%", "count": 0},
        {"range": "21-40%", "count": 0},
        {"range": "41-60%", "count": 0},
        {"range": "61-80%", "count": 0},
        {"range": "81-100%", "count": 0},
    ]
    labels = ["0-20%", "21-40%", "41-60%", "61-80%", "81-100%"]
    for i, r in enumerate(score_result):
        if i < len(score_distribution):
            score_distribution[i]["count"] = r["count"]

    return {
        "dau": dau,
        "wau": wau,
        "questions_served": questions_served,
        "questions_answered": questions_answered,
        "avg_response_time": avg_response_time,
        "completion_rate": completion_rate,
        "peak_hours": peak_hours,
        "dropoff": dropoff,
        "avg_questions_per_session": avg_questions_per_session,
        "daily_activity": daily_activity,
        "score_distribution": score_distribution,
        "total_started": total_started,
        "total_completed": total_completed,
        "total_abandoned": dropoff.get("quiz_abandoned", 0),
    }

@router.get("/daily-active-users")
async def daily_active_users():
    today = datetime.utcnow().date().isoformat()
    pipeline = [
        {"$match": {"date": today}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "count"}
    ]
    result = await analytics_col.aggregate(pipeline).to_list(1)
    return {"date": today, "dau": result[0]["count"] if result else 0}

@router.get("/weekly-active-users")
async def weekly_active_users():
    pipeline = [
        {"$match": {"timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "count"}
    ]
    result = await analytics_col.aggregate(pipeline).to_list(1)
    return {"wau": result[0]["count"] if result else 0}

@router.get("/questions-served")
async def questions_served():
    count = await analytics_col.count_documents({"event": "question_answered"})
    return {"questions_served": count}

@router.get("/avg-response-time")
async def avg_response_time():
    pipeline = [
        {"$match": {"event": "question_answered"}},
        {"$group": {"_id": None, "avg": {"$avg": "$response_duration_seconds"}}}
    ]
    result = await analytics_col.aggregate(pipeline).to_list(1)
    return {"avg_response_time_seconds": round(result[0]["avg"], 2) if result and result[0]["avg"] else 0}

@router.get("/completion-rate")
async def completion_rate():
    started = await analytics_col.count_documents({"event": "quiz_started"})
    completed = await analytics_col.count_documents({"event": "quiz_completed"})
    rate = round((completed / started * 100), 1) if started > 0 else 0
    return {"started": started, "completed": completed, "completion_rate": rate}

@router.get("/peak-hours")
async def peak_hours():
    pipeline = [
        {"$group": {"_id": "$hour", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    result = await analytics_col.aggregate(pipeline).to_list(24)
    return [{"hour": r["_id"], "count": r["count"]} for r in result if r["_id"] is not None]

@router.get("/dropoff")
async def dropoff_analysis():
    pipeline = [
        {"$match": {"event": {"$in": ["quiz_started", "quiz_completed", "quiz_abandoned"]}}},
        {"$group": {"_id": "$event", "count": {"$sum": 1}}}
    ]
    result = await analytics_col.aggregate(pipeline).to_list(10)
    return {r["_id"]: r["count"] for r in result}
