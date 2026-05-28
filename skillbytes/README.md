# SkillBytes — WhatsApp-Style Quiz Platform

A full-stack quiz application built with React, FastAPI, and MongoDB.

## Tech Stack
- **Frontend**: React 18, React Router v6, Recharts, Axios
- **Backend**: FastAPI, Motor (async MongoDB), Pydantic v2
- **Database**: MongoDB 7
- **Containerization**: Docker + Docker Compose

## Features
- 📱 WhatsApp-style chat quiz UI
- 📊 Analytics dashboard with 8+ metrics
- ⏱ Per-question time tracking
- 🏆 Detailed result screen with score ring
- 🌙 Dark theme with modern design
- 📱 Fully responsive UI

## Flow
Exam → Subject → Chapter → Quiz → Result

---

## Quick Start (Recommended — Docker)

```bash
# Clone / extract the project
cd skillbytes

# Start everything
docker-compose up --build

# Open in browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## Manual Setup

### 1. MongoDB
Make sure MongoDB is running locally on port 27017.

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy env file
cp .env.example .env

# Run
uvicorn main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm start
# Runs on http://localhost:3000
```

---

## Seed Demo Data

Once both services are running:

1. Open http://localhost:3000
2. Click **"Seed Demo Data"** on the user selection screen
3. Select a user profile and start quizzing!

Or via API:
```bash
curl -X POST http://localhost:8000/api/seed/
```

This creates:
- 8 users
- 4 exams (UPSC, JEE, NEET, CAT)
- 12+ subjects
- 20+ chapters
- 30+ questions with explanations
- 14 days of historical quiz sessions and analytics

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/exams/ | List all exams |
| GET | /api/subjects/?exam_id= | Subjects by exam |
| GET | /api/chapters/?subject_id= | Chapters by subject |
| POST | /api/quiz/start | Start a quiz session |
| GET | /api/quiz/session/{id}/question | Get current question |
| POST | /api/quiz/answer | Submit an answer |
| POST | /api/quiz/complete | Complete the quiz |
| GET | /api/analytics/dashboard | Full analytics dashboard |
| POST | /api/seed/ | Seed demo data |

Full Swagger docs: http://localhost:8000/docs

---

## Analytics Tracked

1. **Daily Active Users** — unique users per day
2. **Weekly Active Users** — unique users per week
3. **Questions Served** — total questions shown
4. **Questions Answered** — total answers submitted
5. **Average Response Time** — mean time per answer (seconds)
6. **Quiz Completion Rate** — % of started quizzes completed
7. **Drop-off Analysis** — started vs completed vs abandoned
8. **Peak Activity Hours** — activity heatmap by hour
9. **Average Questions per Session**
10. **Score Distribution** — histogram of scores

---

## Database Schema

```
users          → _id, name, email, avatar, created_at
exams          → _id, title, description, icon, color, created_at
subjects       → _id, exam_id, title, description, icon, created_at
chapters       → _id, subject_id, exam_id, title, description, order, created_at
questions      → _id, chapter_id, subject_id, exam_id, text, options[], correct_option_id, explanation, difficulty, created_at
quiz_sessions  → _id, user_id, exam_id, subject_id, chapter_id, started_at, completed_at, status, answers[], score, avg_response_time
analytics      → _id, event, user_id, session_id, question_id, timestamp, date, hour, is_correct, response_duration_seconds, ...
```

---

## Project Structure

```
skillbytes/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── database/connection.py
│   ├── models/schemas.py
│   ├── utils/helpers.py
│   └── routers/
│       ├── exams.py
│       ├── subjects.py
│       ├── chapters.py
│       ├── questions.py
│       ├── quiz.py
│       ├── analytics.py
│       └── seed.py
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── utils/api.js
│   │   ├── styles/global.css
│   │   ├── components/layout/
│   │   └── pages/
│   │       ├── UserSelectPage.js
│   │       ├── HomePage.js
│   │       ├── ExamPage.js
│   │       ├── SubjectsPage.js
│   │       ├── ChaptersPage.js
│   │       ├── QuizPage.js
│   │       ├── ResultPage.js
│   │       └── AnalyticsPage.js
│   ├── Dockerfile
│   └── nginx.conf
└── docker-compose.yml
```
