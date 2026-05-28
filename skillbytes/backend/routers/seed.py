from fastapi import APIRouter
from database.connection import (
    users_col, exams_col, subjects_col, chapters_col,
    questions_col, quiz_sessions_col, analytics_col
)
from utils.helpers import serialize_doc
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.post("/")
async def seed_database():
    # Clear existing data
    await users_col.delete_many({})
    await exams_col.delete_many({})
    await subjects_col.delete_many({})
    await chapters_col.delete_many({})
    await questions_col.delete_many({})
    await quiz_sessions_col.delete_many({})
    await analytics_col.delete_many({})

    now = datetime.utcnow()

    # --- USERS ---
    user_names = [
        ("Arjun Sharma", "arjun@example.com", "🧑"),
        ("Priya Patel", "priya@example.com", "👩"),
        ("Rahul Gupta", "rahul@example.com", "👨"),
        ("Ananya Singh", "ananya@example.com", "👩‍💼"),
        ("Vikram Nair", "vikram@example.com", "🧑‍💻"),
        ("Sneha Reddy", "sneha@example.com", "👩‍🎓"),
        ("Karthik Kumar", "karthik@example.com", "👨‍🔬"),
        ("Divya Iyer", "divya@example.com", "👩‍🏫"),
    ]
    users = []
    for name, email, avatar in user_names:
        r = await users_col.insert_one({
            "name": name, "email": email, "avatar": avatar,
            "created_at": now - timedelta(days=random.randint(5, 60))
        })
        users.append(str(r.inserted_id))

    # --- EXAMS ---
    exam_data = [
        {"title": "UPSC Civil Services", "description": "Union Public Service Commission exam for IAS/IPS/IFS", "icon": "🏛️", "color": "#6366f1"},
        {"title": "JEE Advanced", "description": "Joint Entrance Examination for IITs", "icon": "⚡", "color": "#f59e0b"},
        {"title": "NEET", "description": "National Eligibility cum Entrance Test for medical", "icon": "🏥", "color": "#10b981"},
        {"title": "CAT", "description": "Common Admission Test for IIMs", "icon": "📊", "color": "#ef4444"},
    ]
    exams = []
    for e in exam_data:
        r = await exams_col.insert_one({**e, "created_at": now - timedelta(days=90)})
        exams.append(str(r.inserted_id))

    # --- SUBJECTS per EXAM ---
    subject_map = {}
    subject_defs = {
        exams[0]: [  # UPSC
            ("History", "Ancient to Modern Indian History", "📜"),
            ("Polity", "Indian Constitution & Governance", "⚖️"),
            ("Geography", "Physical & Human Geography", "🌍"),
            ("Economy", "Indian & World Economy", "💹"),
        ],
        exams[1]: [  # JEE
            ("Mathematics", "Calculus, Algebra, Coordinate Geometry", "📐"),
            ("Physics", "Mechanics, Thermodynamics, Optics", "⚛️"),
            ("Chemistry", "Organic, Inorganic & Physical Chemistry", "🧪"),
        ],
        exams[2]: [  # NEET
            ("Biology", "Botany and Zoology", "🌿"),
            ("Physics", "NEET Physics", "⚛️"),
            ("Chemistry", "NEET Chemistry", "🧪"),
        ],
        exams[3]: [  # CAT
            ("Quantitative Aptitude", "Number systems, Algebra, Geometry", "🔢"),
            ("Verbal Ability", "Reading Comprehension, Grammar", "📝"),
            ("Data Interpretation", "Charts, Graphs, Data Analysis", "📊"),
        ]
    }
    
    subjects = {}
    for exam_id, subs in subject_defs.items():
        subjects[exam_id] = []
        for title, desc, icon in subs:
            r = await subjects_col.insert_one({
                "exam_id": exam_id, "title": title, "description": desc,
                "icon": icon, "created_at": now - timedelta(days=80)
            })
            subjects[exam_id].append(str(r.inserted_id))

    # --- CHAPTERS ---
    chapter_map = {}
    chapter_defs = {
        # UPSC History chapters
        (exams[0], subjects[exams[0]][0]): [
            ("Indus Valley Civilization", "Bronze age civilization"),
            ("Vedic Period", "Early and Later Vedic Age"),
            ("Mauryan Empire", "Rise and fall of Mauryas"),
            ("Mughal Empire", "Babur to Aurangzeb"),
        ],
        # UPSC Polity chapters
        (exams[0], subjects[exams[0]][1]): [
            ("Fundamental Rights", "Articles 12-35"),
            ("Directive Principles", "Articles 36-51"),
            ("Parliament", "Lok Sabha and Rajya Sabha"),
        ],
        # JEE Mathematics
        (exams[1], subjects[exams[1]][0]): [
            ("Limits and Continuity", "Calculus basics"),
            ("Differentiation", "Derivatives and applications"),
            ("Integration", "Definite and indefinite integrals"),
        ],
        # JEE Physics
        (exams[1], subjects[exams[1]][1]): [
            ("Kinematics", "Motion in 1D and 2D"),
            ("Laws of Motion", "Newton's laws"),
            ("Work Energy Power", "Energy theorems"),
        ],
        # NEET Biology
        (exams[2], subjects[exams[2]][0]): [
            ("Cell Biology", "Cell structure and function"),
            ("Genetics", "Mendelian genetics and DNA"),
            ("Ecology", "Ecosystems and biodiversity"),
        ],
        # CAT Quant
        (exams[3], subjects[exams[3]][0]): [
            ("Number Systems", "Integers, fractions, decimals"),
            ("Percentages", "Percentage calculations"),
            ("Time and Work", "Work rate problems"),
        ],
    }
    
    chapters = {}
    for (exam_id, subject_id), chaps in chapter_defs.items():
        chapters[(exam_id, subject_id)] = []
        for i, (title, desc) in enumerate(chaps):
            r = await chapters_col.insert_one({
                "exam_id": exam_id, "subject_id": subject_id,
                "title": title, "description": desc, "order": i+1,
                "created_at": now - timedelta(days=70)
            })
            chapters[(exam_id, subject_id)].append(str(r.inserted_id))

    # --- QUESTIONS ---
    all_question_sets = {
        # UPSC History - Indus Valley
        (exams[0], subjects[exams[0]][0], 0): [
            {
                "text": "Which of the following is the largest site of the Indus Valley Civilization?",
                "options": [
                    {"id": "a", "text": "Harappa"}, {"id": "b", "text": "Mohenjo-daro"},
                    {"id": "c", "text": "Rakhigarhi"}, {"id": "d", "text": "Dholavira"}
                ],
                "correct": "c",
                "explanation": "Rakhigarhi in Haryana is the largest known IVC site, larger than Mohenjo-daro.",
                "difficulty": "medium"
            },
            {
                "text": "The Great Bath of Mohenjo-daro was used for:",
                "options": [
                    {"id": "a", "text": "Recreation"}, {"id": "b", "text": "Ritual bathing"},
                    {"id": "c", "text": "Water storage"}, {"id": "d", "text": "Fish farming"}
                ],
                "correct": "b",
                "explanation": "The Great Bath is believed to have been used for ritual purification ceremonies.",
                "difficulty": "easy"
            },
            {
                "text": "The Indus Valley Civilization is also known as:",
                "options": [
                    {"id": "a", "text": "Vedic Civilization"}, {"id": "b", "text": "Harappan Civilization"},
                    {"id": "c", "text": "Dravidian Civilization"}, {"id": "d", "text": "Aryan Civilization"}
                ],
                "correct": "b",
                "explanation": "Harappan Civilization is named after Harappa, the first site discovered.",
                "difficulty": "easy"
            },
            {
                "text": "Which river was NOT associated with the Indus Valley Civilization?",
                "options": [
                    {"id": "a", "text": "Indus"}, {"id": "b", "text": "Saraswati"},
                    {"id": "c", "text": "Ganga"}, {"id": "d", "text": "Ravi"}
                ],
                "correct": "c",
                "explanation": "The IVC was primarily located around the Indus and Saraswati rivers, not the Ganga.",
                "difficulty": "medium"
            },
            {
                "text": "Dholavira is located in present-day:",
                "options": [
                    {"id": "a", "text": "Punjab"}, {"id": "b", "text": "Rajasthan"},
                    {"id": "c", "text": "Gujarat"}, {"id": "d", "text": "Haryana"}
                ],
                "correct": "c",
                "explanation": "Dholavira is located in the Kutch district of Gujarat.",
                "difficulty": "hard"
            },
        ],
        # UPSC Polity - Fundamental Rights
        (exams[0], subjects[exams[0]][1], 0): [
            {
                "text": "Right to Education (Article 21A) was added by which Constitutional Amendment?",
                "options": [
                    {"id": "a", "text": "86th Amendment"}, {"id": "b", "text": "42nd Amendment"},
                    {"id": "c", "text": "44th Amendment"}, {"id": "d", "text": "73rd Amendment"}
                ],
                "correct": "a",
                "explanation": "The 86th Constitutional Amendment Act, 2002 inserted Article 21A.",
                "difficulty": "medium"
            },
            {
                "text": "Which Article of the Constitution abolishes untouchability?",
                "options": [
                    {"id": "a", "text": "Article 14"}, {"id": "b", "text": "Article 17"},
                    {"id": "c", "text": "Article 21"}, {"id": "d", "text": "Article 19"}
                ],
                "correct": "b",
                "explanation": "Article 17 of the Indian Constitution abolishes untouchability.",
                "difficulty": "easy"
            },
            {
                "text": "Fundamental Rights are enshrined in which Part of the Constitution?",
                "options": [
                    {"id": "a", "text": "Part II"}, {"id": "b", "text": "Part III"},
                    {"id": "c", "text": "Part IV"}, {"id": "d", "text": "Part I"}
                ],
                "correct": "b",
                "explanation": "Fundamental Rights are contained in Part III (Articles 12–35) of the Constitution.",
                "difficulty": "easy"
            },
            {
                "text": "The right to form associations or unions is guaranteed under:",
                "options": [
                    {"id": "a", "text": "Article 19(1)(b)"}, {"id": "b", "text": "Article 19(1)(c)"},
                    {"id": "c", "text": "Article 19(1)(a)"}, {"id": "d", "text": "Article 19(1)(d)"}
                ],
                "correct": "b",
                "explanation": "Article 19(1)(c) guarantees the right to form associations or unions.",
                "difficulty": "hard"
            },
            {
                "text": "Which of the following is NOT a Fundamental Right?",
                "options": [
                    {"id": "a", "text": "Right to Equality"}, {"id": "b", "text": "Right to Property"},
                    {"id": "c", "text": "Right against Exploitation"}, {"id": "d", "text": "Right to Freedom"}
                ],
                "correct": "b",
                "explanation": "Right to Property was removed from Fundamental Rights by the 44th Amendment, 1978.",
                "difficulty": "medium"
            },
        ],
        # JEE Mathematics - Limits
        (exams[1], subjects[exams[1]][0], 0): [
            {
                "text": "What is the value of lim(x→0) sin(x)/x?",
                "options": [
                    {"id": "a", "text": "0"}, {"id": "b", "text": "∞"},
                    {"id": "c", "text": "1"}, {"id": "d", "text": "Undefined"}
                ],
                "correct": "c",
                "explanation": "This is a standard limit. As x approaches 0, sin(x)/x approaches 1.",
                "difficulty": "easy"
            },
            {
                "text": "lim(x→∞) (1 + 1/x)^x equals:",
                "options": [
                    {"id": "a", "text": "1"}, {"id": "b", "text": "e"},
                    {"id": "c", "text": "∞"}, {"id": "d", "text": "0"}
                ],
                "correct": "b",
                "explanation": "This is the definition of Euler's number e ≈ 2.71828.",
                "difficulty": "medium"
            },
            {
                "text": "A function f(x) is continuous at x = a if:",
                "options": [
                    {"id": "a", "text": "f(a) is defined"}, {"id": "b", "text": "lim(x→a) f(x) exists"},
                    {"id": "c", "text": "lim(x→a) f(x) = f(a)"}, {"id": "d", "text": "f'(a) exists"}
                ],
                "correct": "c",
                "explanation": "Continuity requires that the limit equals the function value at that point.",
                "difficulty": "easy"
            },
            {
                "text": "lim(x→0) (e^x - 1)/x equals:",
                "options": [
                    {"id": "a", "text": "0"}, {"id": "b", "text": "e"},
                    {"id": "c", "text": "1"}, {"id": "d", "text": "∞"}
                ],
                "correct": "c",
                "explanation": "Using L'Hôpital's rule or Taylor series expansion, this limit equals 1.",
                "difficulty": "medium"
            },
            {
                "text": "Which of the following is a removable discontinuity?",
                "options": [
                    {"id": "a", "text": "lim does not exist"}, {"id": "b", "text": "f(a) is undefined but limit exists"},
                    {"id": "c", "text": "Infinite discontinuity"}, {"id": "d", "text": "Jump discontinuity"}
                ],
                "correct": "b",
                "explanation": "Removable discontinuity occurs when the limit exists but f(a) is undefined or differs.",
                "difficulty": "hard"
            },
        ],
        # NEET Biology - Cell Biology
        (exams[2], subjects[exams[2]][0], 0): [
            {
                "text": "Which organelle is known as the 'powerhouse of the cell'?",
                "options": [
                    {"id": "a", "text": "Nucleus"}, {"id": "b", "text": "Mitochondria"},
                    {"id": "c", "text": "Ribosome"}, {"id": "d", "text": "Golgi apparatus"}
                ],
                "correct": "b",
                "explanation": "Mitochondria produce ATP through cellular respiration, earning the powerhouse title.",
                "difficulty": "easy"
            },
            {
                "text": "The fluid mosaic model of cell membrane was proposed by:",
                "options": [
                    {"id": "a", "text": "Watson and Crick"}, {"id": "b", "text": "Singer and Nicolson"},
                    {"id": "c", "text": "Schleiden and Schwann"}, {"id": "d", "text": "Virchow"}
                ],
                "correct": "b",
                "explanation": "Singer and Nicolson proposed the fluid mosaic model in 1972.",
                "difficulty": "medium"
            },
            {
                "text": "Ribosomes are composed of:",
                "options": [
                    {"id": "a", "text": "DNA and protein"}, {"id": "b", "text": "RNA and lipids"},
                    {"id": "c", "text": "rRNA and proteins"}, {"id": "d", "text": "DNA and lipids"}
                ],
                "correct": "c",
                "explanation": "Ribosomes are made of ribosomal RNA (rRNA) and proteins.",
                "difficulty": "easy"
            },
            {
                "text": "Which cell organelle is responsible for protein synthesis?",
                "options": [
                    {"id": "a", "text": "Lysosome"}, {"id": "b", "text": "Ribosome"},
                    {"id": "c", "text": "Centrosome"}, {"id": "d", "text": "Vacuole"}
                ],
                "correct": "b",
                "explanation": "Ribosomes are the sites of protein synthesis in the cell.",
                "difficulty": "easy"
            },
            {
                "text": "Plant cells are distinguished from animal cells by the presence of:",
                "options": [
                    {"id": "a", "text": "Mitochondria"}, {"id": "b", "text": "Cell membrane"},
                    {"id": "c", "text": "Cell wall and chloroplasts"}, {"id": "d", "text": "Ribosomes"}
                ],
                "correct": "c",
                "explanation": "Cell wall (made of cellulose) and chloroplasts are present in plant cells but not animal cells.",
                "difficulty": "easy"
            },
        ],
        # CAT Quant - Number Systems
        (exams[3], subjects[exams[3]][0], 0): [
            {
                "text": "What is the LCM of 12, 18, and 24?",
                "options": [
                    {"id": "a", "text": "36"}, {"id": "b", "text": "72"},
                    {"id": "c", "text": "48"}, {"id": "d", "text": "144"}
                ],
                "correct": "b",
                "explanation": "LCM(12,18,24) = 72. Prime factorization: 12=2²×3, 18=2×3², 24=2³×3. LCM=2³×3²=72.",
                "difficulty": "medium"
            },
            {
                "text": "The sum of all integers from 1 to 100 is:",
                "options": [
                    {"id": "a", "text": "4950"}, {"id": "b", "text": "5000"},
                    {"id": "c", "text": "5050"}, {"id": "d", "text": "5100"}
                ],
                "correct": "c",
                "explanation": "Using the formula n(n+1)/2 = 100×101/2 = 5050.",
                "difficulty": "easy"
            },
            {
                "text": "If a number is divisible by both 4 and 6, it must be divisible by:",
                "options": [
                    {"id": "a", "text": "8"}, {"id": "b", "text": "12"},
                    {"id": "c", "text": "24"}, {"id": "d", "text": "16"}
                ],
                "correct": "b",
                "explanation": "LCM(4,6) = 12. A number divisible by both 4 and 6 must be divisible by their LCM, which is 12.",
                "difficulty": "medium"
            },
            {
                "text": "What is the remainder when 2^10 is divided by 10?",
                "options": [
                    {"id": "a", "text": "2"}, {"id": "b", "text": "4"},
                    {"id": "c", "text": "6"}, {"id": "d", "text": "8"}
                ],
                "correct": "b",
                "explanation": "2^10 = 1024. 1024 ÷ 10 gives remainder 4.",
                "difficulty": "medium"
            },
            {
                "text": "A prime number is:",
                "options": [
                    {"id": "a", "text": "Divisible by 2"}, {"id": "b", "text": "Divisible by 1 only"},
                    {"id": "c", "text": "Divisible by exactly 2 factors"}, {"id": "d", "text": "An even number"}
                ],
                "correct": "c",
                "explanation": "A prime number has exactly two factors: 1 and itself.",
                "difficulty": "easy"
            },
        ],
    }

    q_ids_by_chapter = {}
    for (exam_id, subject_id, chap_idx), q_list in all_question_sets.items():
        key = (exam_id, subject_id)
        if key in chapters and chap_idx < len(chapters[key]):
            chapter_id = chapters[key][chap_idx]
            q_ids_by_chapter[chapter_id] = []
            for q in q_list:
                r = await questions_col.insert_one({
                    "exam_id": exam_id,
                    "subject_id": subject_id,
                    "chapter_id": chapter_id,
                    "text": q["text"],
                    "options": q["options"],
                    "correct_option_id": q["correct"],
                    "explanation": q["explanation"],
                    "difficulty": q["difficulty"],
                    "created_at": now - timedelta(days=60)
                })
                q_ids_by_chapter[chapter_id].append(str(r.inserted_id))

    # --- QUIZ SESSIONS (historical data) ---
    all_chapter_ids = list(q_ids_by_chapter.keys())
    for day_offset in range(14, -1, -1):
        num_sessions = random.randint(3, 12)
        session_date = now - timedelta(days=day_offset)
        for _ in range(num_sessions):
            user_id = random.choice(users)
            chapter_id = random.choice(all_chapter_ids)
            q_ids = q_ids_by_chapter[chapter_id]
            if not q_ids:
                continue

            # Find exam and subject for this chapter
            chap_doc = await chapters_col.find_one({"_id": __import__('bson').ObjectId(chapter_id)})
            if not chap_doc:
                continue
            exam_id = chap_doc["exam_id"]
            subject_id = chap_doc["subject_id"]

            started_at = session_date.replace(
                hour=random.choice([8, 9, 10, 14, 15, 16, 19, 20, 21]),
                minute=random.randint(0, 59)
            )
            status = random.choices(["completed", "abandoned"], weights=[0.75, 0.25])[0]
            num_answered = len(q_ids) if status == "completed" else random.randint(1, max(1, len(q_ids)-1))

            answers = []
            for i in range(num_answered):
                q = await questions_col.find_one({"_id": __import__('bson').ObjectId(q_ids[i])})
                if not q:
                    continue
                shown_at = started_at + timedelta(seconds=i * random.randint(20, 90))
                duration = random.uniform(5, 60)
                sub_at = shown_at + timedelta(seconds=duration)
                is_correct = random.random() > 0.4
                selected = q["correct_option_id"] if is_correct else random.choice([o["id"] for o in q["options"] if o["id"] != q["correct_option_id"]] or [q["correct_option_id"]])
                answers.append({
                    "question_id": q_ids[i],
                    "selected_option_id": selected,
                    "correct_option_id": q["correct_option_id"],
                    "is_correct": selected == q["correct_option_id"],
                    "question_shown_at": shown_at,
                    "answer_submitted_at": sub_at,
                    "response_duration_seconds": duration
                })

            correct = sum(1 for a in answers if a["is_correct"])
            score = (correct / len(q_ids) * 100) if len(q_ids) > 0 else 0
            avg_rt = sum(a["response_duration_seconds"] for a in answers) / len(answers) if answers else 0
            completed_at = started_at + timedelta(seconds=len(answers) * 40) if status == "completed" else None

            r = await quiz_sessions_col.insert_one({
                "user_id": user_id,
                "exam_id": exam_id,
                "subject_id": subject_id,
                "chapter_id": chapter_id,
                "started_at": started_at,
                "completed_at": completed_at,
                "status": status,
                "question_ids": q_ids,
                "current_question_index": num_answered,
                "answers": answers,
                "score": score if status == "completed" else None,
                "correct_answers": correct,
                "total_questions": len(q_ids),
                "avg_response_time": avg_rt
            })
            session_id = str(r.inserted_id)

            # Analytics events
            await analytics_col.insert_one({
                "event": "quiz_started", "user_id": user_id,
                "exam_id": exam_id, "subject_id": subject_id,
                "chapter_id": chapter_id, "session_id": session_id,
                "timestamp": started_at, "hour": started_at.hour,
                "date": started_at.date().isoformat()
            })
            for ans in answers:
                await analytics_col.insert_one({
                    "event": "question_answered", "user_id": user_id,
                    "session_id": session_id, "question_id": ans["question_id"],
                    "is_correct": ans["is_correct"],
                    "response_duration_seconds": ans["response_duration_seconds"],
                    "timestamp": ans["answer_submitted_at"],
                    "hour": ans["answer_submitted_at"].hour,
                    "date": ans["answer_submitted_at"].date().isoformat()
                })
            if status == "completed":
                await analytics_col.insert_one({
                    "event": "quiz_completed", "user_id": user_id,
                    "session_id": session_id, "score": score,
                    "correct_answers": correct, "total_questions": len(q_ids),
                    "avg_response_time": avg_rt, "timestamp": completed_at,
                    "date": completed_at.date().isoformat()
                })
            else:
                await analytics_col.insert_one({
                    "event": "quiz_abandoned", "user_id": user_id,
                    "session_id": session_id,
                    "questions_answered": num_answered,
                    "total_questions": len(q_ids),
                    "timestamp": started_at + timedelta(seconds=num_answered * 40),
                    "date": started_at.date().isoformat()
                })

    return {
        "message": "Database seeded successfully",
        "users": len(users),
        "exams": len(exam_data),
        "subjects": sum(len(v) for v in subjects.values()),
        "chapters": sum(len(v) for v in chapters.values()),
        "questions": sum(len(v) for v in q_ids_by_chapter.values()),
        "users_list": [{"id": uid, "name": n} for uid, (n, e, a) in zip(users, user_names)]
    }

@router.get("/users")
async def get_users():
    users = await users_col.find().to_list(100)
    from utils.helpers import serialize_list
    return serialize_list(users)
