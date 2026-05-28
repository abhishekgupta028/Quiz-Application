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
- 13 subjects
- 40 chapters
- 200 questions with explanations, difficulty levels, and answer options
- 14+ days of historical quiz sessions and analytics data

---

## 📸 Application Screenshots & MongoDB Data

The `skillbyte_SS/` folder contains comprehensive screenshots demonstrating:

### 🎯 User Interface Flow

**Screenshot 128** - User Selection Page
- Shows all 8 seeded users with their profiles
- Avatar icons and email addresses
- "Reseed Database" button to refresh data
- Multi-user support for testing

**Screenshot 129** - Home Dashboard
- Welcome message with user name
- 4 available exams (UPSC, JEE, NEET, CAT)
- Quick stats: 4 Exams, ∞ Questions
- Sidebar with Exams and Analytics navigation

**Screenshot 130** - Exam Subjects Page (JEE Example)
- JEE Advanced exam details
- 3 subjects: Mathematics, Physics, Chemistry
- Subject descriptions and icons
- Clickable subject cards to access chapters

**Screenshot 131** - Chapter Selection Page (Physics)
- Physics subject overview
- 3 chapters with detailed descriptions:
  - Kinematics (Motion in 1D and 2D)
  - Laws of Motion (Newton's laws)
  - Work Energy Power (Energy theorems)
- "Start Quiz" buttons for each chapter
- Chapter ordering and numbering

**Screenshots 132-135** - Quiz Taking Interface
- Individual question display
- Multiple choice options (A, B, C, D)
- Question counter (Q1/5, Q2/5, etc.)
- Option selection highlighting
- Smooth navigation between questions
- Real-time feedback on answer submission

**Screenshot 136** - Quiz Result Screen
- Score visualization with circular progress (40%)
- Correct/Wrong/Average Time metrics (2/5 correct)
- Answer Review section showing:
  - Q1: Correct (green checkmark)
  - Q2-Q5: Wrong (red X marks)
  - Time taken per question
- "Back to Exams" and "View Analytics" buttons

**Screenshot 137** - Analytics Dashboard
- Real-time quiz engagement metrics:
  - **Daily Active Users**: Profile count
  - **Weekly Active Users**: Weekly engagement
  - **Questions Served**: 540+ questions delivered
  - **Questions Answered**: 540+ responses recorded
  - **Avg Response Time**: 252.8 seconds per question
  - **Completion Rate**: 70.6% (58/138 quizzes)
  - **Avg Questions/Session**: 5 questions
  - **Abandoned Quizzes**: 25 sessions not completed
- **Daily Quiz Activity Chart**: 14-day trend line showing usage patterns
- **Quiz Drop-off Analysis**: 140 started, 100 completed, 40 abandoned
- **Peak Activity Hours & Score Distribution** sections

### 🗄️ MongoDB Data Verification

**Screenshot 140** - Questions Collection
- MongoDB aggregation query: `db.questions.aggregate([{ $group: { _id: "$chapter_id", count: { $sum: 1 } } }])`
- Verification results showing:
  - **Each chapter has exactly 5 questions**
  - **40 chapters total** with questions properly mapped
  - Sample chapter IDs with their corresponding question counts
- Quiz sessions data showing:
  - user_id, exam_id, subject_id, chapter_id linking
  - started_at timestamp tracking
  - status: "abandoned" or "in_progress"
  - question_ids array with question references

**Screenshot 141** - Analytics Collection & Quiz Sessions
- Analytics events tracking:
  - **quiz_started** event: User initiates quiz with timestamp, exam/subject/chapter context
  - **question_answered** event: Individual question responses with:
    - is_correct: true/false flag
    - response_duration_seconds: Time taken
    - timestamp: Exact answer time
- Quiz sessions showing:
  - total_questions: 5
  - avg_response_time: 30.74 seconds per question
  - Complete quiz session data structure

**Screenshot 142** - Database Summary & Collection Counts
- MongoDB count verification:
  ```
  db.subjects.countDocuments()      → 13 subjects
  db.chapters.countDocuments()       → 40 chapters  
  db.questions.countDocuments()      → 200 questions
  db.quiz_sessions.countDocuments()  → [historical sessions]
  db.analytics.countDocuments()      → 797 events
  ```
- Analytics events showing:
  - Complete quiz_started, question_answered, quiz_completed tracking
  - Per-question response time measurement
  - Correct/incorrect answer validation
- Database integrity verification confirming all collections properly seeded

### 📊 Data Integrity Verification

The screenshots confirm:
✅ **All 40 chapters have exactly 5 questions each** (200 total questions)
✅ **4 exams properly structured** with subjects and chapters
✅ **8 seeded users** with profile data
✅ **Analytics tracking working** (797+ events recorded)
✅ **Quiz sessions storing** user responses and timing data
✅ **Answer correctness** properly validated and tracked
✅ **No missing chapters** - all chapters accessible and quizzable

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
