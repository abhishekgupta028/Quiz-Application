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
        # UPSC Geography chapters
        (exams[0], subjects[exams[0]][2]): [
            ("Physical Geography", "Landforms and climate"),
            ("Human Geography", "Population and settlement"),
            ("Biogeography", "Flora and fauna distribution"),
        ],
        # UPSC Economy chapters
        (exams[0], subjects[exams[0]][3]): [
            ("Microeconomics", "Supply, demand and markets"),
            ("Macroeconomics", "GDP, inflation and growth"),
            ("International Trade", "Exports, imports and tariffs"),
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
        # JEE Chemistry
        (exams[1], subjects[exams[1]][2]): [
            ("Atomic Structure", "Electrons, orbitals, quantum numbers"),
            ("Chemical Bonding", "Ionic, covalent and metallic bonds"),
            ("Periodic Table", "Properties and trends"),
        ],
        # NEET Biology
        (exams[2], subjects[exams[2]][0]): [
            ("Cell Biology", "Cell structure and function"),
            ("Genetics", "Mendelian genetics and DNA"),
            ("Ecology", "Ecosystems and biodiversity"),
        ],
        # NEET Physics
        (exams[2], subjects[exams[2]][1]): [
            ("Mechanics", "Motion and forces"),
            ("Optics", "Light and lenses"),
            ("Modern Physics", "Atoms and radiation"),
        ],
        # NEET Chemistry
        (exams[2], subjects[exams[2]][2]): [
            ("Inorganic Chemistry", "Elements and compounds"),
            ("Organic Chemistry", "Carbon compounds and reactions"),
            ("Physical Chemistry", "Thermodynamics and equilibrium"),
        ],
        # CAT Quant
        (exams[3], subjects[exams[3]][0]): [
            ("Number Systems", "Integers, fractions, decimals"),
            ("Percentages", "Percentage calculations"),
            ("Time and Work", "Work rate problems"),
        ],
        # CAT Verbal
        (exams[3], subjects[exams[3]][1]): [
            ("Reading Comprehension", "Passages and questions"),
            ("Grammar", "Sentence correction"),
            ("Vocabulary", "Word meanings and usage"),
        ],
        # CAT Data Interpretation
        (exams[3], subjects[exams[3]][2]): [
            ("Pie Charts", "Circular diagram analysis"),
            ("Bar Graphs", "Column and bar chart analysis"),
            ("Tables", "Data table interpretation"),
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

    # --- COMPREHENSIVE QUESTIONS FOR ALL CHAPTERS ---
    all_question_sets = {
        # UPSC History - Chapter 0: Indus Valley
        (exams[0], subjects[exams[0]][0], 0): [
            {"text": "Which of the following is the largest site of the Indus Valley Civilization?", "options": [{"id": "a", "text": "Harappa"}, {"id": "b", "text": "Mohenjo-daro"}, {"id": "c", "text": "Rakhigarhi"}, {"id": "d", "text": "Dholavira"}], "correct": "c", "explanation": "Rakhigarhi in Haryana is the largest known IVC site.", "difficulty": "medium"},
            {"text": "The Great Bath of Mohenjo-daro was used for:", "options": [{"id": "a", "text": "Recreation"}, {"id": "b", "text": "Ritual bathing"}, {"id": "c", "text": "Water storage"}, {"id": "d", "text": "Fish farming"}], "correct": "b", "explanation": "The Great Bath is believed to have been used for ritual purification.", "difficulty": "easy"},
            {"text": "The Indus Valley Civilization is also known as:", "options": [{"id": "a", "text": "Vedic Civilization"}, {"id": "b", "text": "Harappan Civilization"}, {"id": "c", "text": "Dravidian Civilization"}, {"id": "d", "text": "Aryan Civilization"}], "correct": "b", "explanation": "Harappan Civilization is named after Harappa, the first site discovered.", "difficulty": "easy"},
            {"text": "Which river was NOT associated with the Indus Valley Civilization?", "options": [{"id": "a", "text": "Indus"}, {"id": "b", "text": "Saraswati"}, {"id": "c", "text": "Ganga"}, {"id": "d", "text": "Ravi"}], "correct": "c", "explanation": "The IVC was primarily around Indus and Saraswati rivers, not Ganga.", "difficulty": "medium"},
            {"text": "Dholavira is located in present-day:", "options": [{"id": "a", "text": "Punjab"}, {"id": "b", "text": "Rajasthan"}, {"id": "c", "text": "Gujarat"}, {"id": "d", "text": "Haryana"}], "correct": "c", "explanation": "Dholavira is located in the Kutch district of Gujarat.", "difficulty": "hard"},
        ],
        # UPSC History - Chapter 1: Vedic Period
        (exams[0], subjects[exams[0]][0], 1): [
            {"text": "The Vedas were composed during which period?", "options": [{"id": "a", "text": "1500-500 BC"}, {"id": "b", "text": "2000-1000 BC"}, {"id": "c", "text": "1000-500 BC"}, {"id": "d", "text": "3000-1500 BC"}], "correct": "a", "explanation": "The Vedic period is generally dated from 1500-500 BC.", "difficulty": "medium"},
            {"text": "Which Veda contains hymns about nature and gods?", "options": [{"id": "a", "text": "Yajur Veda"}, {"id": "b", "text": "Rig Veda"}, {"id": "c", "text": "Sama Veda"}, {"id": "d", "text": "Atharva Veda"}], "correct": "b", "explanation": "The Rig Veda is the oldest and contains hymns about nature and gods.", "difficulty": "easy"},
            {"text": "The caste system in Vedic period was based on:", "options": [{"id": "a", "text": "Birth"}, {"id": "b", "text": "Occupation"}, {"id": "c", "text": "Wealth"}, {"id": "d", "text": "Education"}], "correct": "b", "explanation": "Initially, the caste system was based on occupation, later became hereditary.", "difficulty": "medium"},
            {"text": "Who were the Aryans?", "options": [{"id": "a", "text": "Indigenous to India"}, {"id": "b", "text": "Nomadic pastoralists from Central Asia"}, {"id": "c", "text": "From Africa"}, {"id": "d", "text": "From Southeast Asia"}], "correct": "b", "explanation": "Aryans were Indo-European pastoralists who migrated to India.", "difficulty": "medium"},
            {"text": "The Vedic period is divided into:", "options": [{"id": "a", "text": "Two phases"}, {"id": "b", "text": "Three phases"}, {"id": "c", "text": "Four phases"}, {"id": "d", "text": "Five phases"}], "correct": "a", "explanation": "Early Vedic (1500-1000 BC) and Later Vedic (1000-500 BC).", "difficulty": "easy"},
        ],
        # UPSC History - Chapter 2: Mauryan Empire
        (exams[0], subjects[exams[0]][0], 2): [
            {"text": "Who founded the Mauryan Empire?", "options": [{"id": "a", "text": "Ashoka"}, {"id": "b", "text": "Chandragupta Maurya"}, {"id": "c", "text": "Bindusara"}, {"id": "d", "text": "Harsha"}], "correct": "b", "explanation": "Chandragupta Maurya founded the Mauryan Empire with help of Chanakya.", "difficulty": "easy"},
            {"text": "Who was Chanakya?", "options": [{"id": "a", "text": "A warrior"}, {"id": "b", "text": "A political advisor and minister"}, {"id": "c", "text": "A priest"}, {"id": "d", "text": "A merchant"}], "correct": "b", "explanation": "Chanakya was a brilliant political advisor to Chandragupta Maurya.", "difficulty": "easy"},
            {"text": "Ashoka's major contribution was:", "options": [{"id": "a", "text": "Expanding the empire"}, {"id": "b", "text": "Spreading Buddhism"}, {"id": "c", "text": "Building cities"}, {"id": "d", "text": "Introducing agriculture"}], "correct": "b", "explanation": "Ashoka became a Buddhist and spread Buddhism throughout Asia.", "difficulty": "medium"},
            {"text": "Ashoka's edicts were inscribed on:", "options": [{"id": "a", "text": "Stone pillars and rocks"}, {"id": "b", "text": "Copper plates"}, {"id": "c", "text": "Palm leaves"}, {"id": "d", "text": "Wooden tablets"}], "correct": "a", "explanation": "Ashoka's edicts were carved on stone pillars and rock faces.", "difficulty": "medium"},
            {"text": "The Mauryan Empire fell around:", "options": [{"id": "a", "text": "300 BC"}, {"id": "b", "text": "200 BC"}, {"id": "c", "text": "100 BC"}, {"id": "d", "text": "50 BC"}], "correct": "c", "explanation": "The Mauryan Empire fell around 185 BC, ending with the Gupta era.", "difficulty": "hard"},
        ],
        # UPSC History - Chapter 3: Mughal Empire
        (exams[0], subjects[exams[0]][0], 3): [
            {"text": "Who was the founder of the Mughal Empire in India?", "options": [{"id": "a", "text": "Akbar"}, {"id": "b", "text": "Babur"}, {"id": "c", "text": "Aurangzeb"}, {"id": "d", "text": "Shah Jahan"}], "correct": "b", "explanation": "Babur founded the Mughal Empire after defeating Ibrahim Lodi in 1526.", "difficulty": "easy"},
            {"text": "Akbar's policy of religious tolerance was called:", "options": [{"id": "a", "text": "Sharia"}, {"id": "b", "text": "Sulh-i-kul"}, {"id": "c", "text": "Dharma"}, {"id": "d", "text": "Fatwa"}], "correct": "b", "explanation": "Sulh-i-kul means 'peace with all' and was Akbar's tolerance policy.", "difficulty": "medium"},
            {"text": "The Taj Mahal was built by:", "options": [{"id": "a", "text": "Akbar"}, {"id": "b", "text": "Babur"}, {"id": "c", "text": "Shah Jahan"}, {"id": "d", "text": "Aurangzeb"}], "correct": "c", "explanation": "Shah Jahan built the Taj Mahal in memory of Mumtaz Mahal.", "difficulty": "easy"},
            {"text": "Aurangzeb's reign marked:", "options": [{"id": "a", "text": "Beginning of Mughal decline"}, {"id": "b", "text": "Peak of Mughal power"}, {"id": "c", "text": "Peace with Marathas"}, {"id": "d", "text": "Alliance with British"}], "correct": "a", "explanation": "Aurangzeb's religious policies and constant wars led to Mughal decline.", "difficulty": "medium"},
            {"text": "The Mughal administration was divided into provinces called:", "options": [{"id": "a", "text": "Jagirs"}, {"id": "b", "text": "Subas"}, {"id": "c", "text": "Pargannas"}, {"id": "d", "text": "Zamindaris"}], "correct": "b", "explanation": "Subas were provinces headed by Subahdars in the Mughal administration.", "difficulty": "hard"},
        ],

        # UPSC Polity - Chapter 0: Fundamental Rights
        (exams[0], subjects[exams[0]][1], 0): [
            {"text": "Right to Education (Article 21A) was added by which Constitutional Amendment?", "options": [{"id": "a", "text": "86th Amendment"}, {"id": "b", "text": "42nd Amendment"}, {"id": "c", "text": "44th Amendment"}, {"id": "d", "text": "73rd Amendment"}], "correct": "a", "explanation": "The 86th Constitutional Amendment Act, 2002 inserted Article 21A.", "difficulty": "medium"},
            {"text": "Which Article of the Constitution abolishes untouchability?", "options": [{"id": "a", "text": "Article 14"}, {"id": "b", "text": "Article 17"}, {"id": "c", "text": "Article 21"}, {"id": "d", "text": "Article 19"}], "correct": "b", "explanation": "Article 17 of the Indian Constitution abolishes untouchability.", "difficulty": "easy"},
            {"text": "Fundamental Rights are enshrined in which Part of the Constitution?", "options": [{"id": "a", "text": "Part II"}, {"id": "b", "text": "Part III"}, {"id": "c", "text": "Part IV"}, {"id": "d", "text": "Part I"}], "correct": "b", "explanation": "Fundamental Rights are contained in Part III (Articles 12–35).", "difficulty": "easy"},
            {"text": "The right to form associations or unions is guaranteed under:", "options": [{"id": "a", "text": "Article 19(1)(b)"}, {"id": "b", "text": "Article 19(1)(c)"}, {"id": "c", "text": "Article 19(1)(a)"}, {"id": "d", "text": "Article 19(1)(d)"}], "correct": "b", "explanation": "Article 19(1)(c) guarantees the right to form associations.", "difficulty": "hard"},
            {"text": "Which is NOT a Fundamental Right?", "options": [{"id": "a", "text": "Right to Equality"}, {"id": "b", "text": "Right to Property"}, {"id": "c", "text": "Right against Exploitation"}, {"id": "d", "text": "Right to Freedom"}], "correct": "b", "explanation": "Right to Property was removed by the 44th Amendment, 1978.", "difficulty": "medium"},
        ],
        # UPSC Polity - Chapter 1: Directive Principles
        (exams[0], subjects[exams[0]][1], 1): [
            {"text": "Directive Principles are enshrined in which Part?", "options": [{"id": "a", "text": "Part III"}, {"id": "b", "text": "Part IV"}, {"id": "c", "text": "Part V"}, {"id": "d", "text": "Part II"}], "correct": "b", "explanation": "Directive Principles are in Part IV (Articles 36-51) of Constitution.", "difficulty": "easy"},
            {"text": "Directive Principles are:", "options": [{"id": "a", "text": "Justiciable"}, {"id": "b", "text": "Non-justiciable"}, {"id": "c", "text": "Partially justiciable"}, {"id": "d", "text": "Conditionally justiciable"}], "correct": "b", "explanation": "Directive Principles are non-justiciable, but guide state policy.", "difficulty": "medium"},
            {"text": "Article 44 of the Directive Principles seeks to establish:", "options": [{"id": "a", "text": "Uniform Civil Code"}, {"id": "b", "text": "Secular State"}, {"id": "c", "text": "Socialist State"}, {"id": "d", "text": "Democratic State"}], "correct": "a", "explanation": "Article 44 seeks to establish a Uniform Civil Code for all citizens.", "difficulty": "medium"},
            {"text": "The objective of Directive Principles is to:", "options": [{"id": "a", "text": "Protect individual rights"}, {"id": "b", "text": "Guide state in framing laws"}, {"id": "c", "text": "Punish criminals"}, {"id": "d", "text": "Define state boundaries"}], "correct": "b", "explanation": "Directive Principles guide the state in framing laws and policies.", "difficulty": "easy"},
            {"text": "Right to free and compulsory education is under:", "options": [{"id": "a", "text": "Fundamental Rights"}, {"id": "b", "text": "Directive Principles"}, {"id": "c", "text": "Right against Exploitation"}, {"id": "d", "text": "Cultural Rights"}], "correct": "b", "explanation": "Initially in Directive Principles, later made Fundamental Right.", "difficulty": "hard"},
        ],
        # UPSC Polity - Chapter 2: Parliament
        (exams[0], subjects[exams[0]][1], 2): [
            {"text": "The Lok Sabha has a maximum of how many members?", "options": [{"id": "a", "text": "545"}, {"id": "b", "text": "552"}, {"id": "c", "text": "542"}, {"id": "d", "text": "550"}], "correct": "b", "explanation": "Lok Sabha has maximum 552 members (530 from states + 20 from UTs + 2 Anglo-Indians).", "difficulty": "medium"},
            {"text": "The Rajya Sabha has how many members?", "options": [{"id": "a", "text": "245"}, {"id": "b", "text": "250"}, {"id": "c", "text": "240"}, {"id": "d", "text": "235"}], "correct": "a", "explanation": "Rajya Sabha has 245 members (233 elected + 12 nominated).", "difficulty": "medium"},
            {"text": "The term of Lok Sabha is:", "options": [{"id": "a", "text": "3 years"}, {"id": "b", "text": "5 years"}, {"id": "c", "text": "4 years"}, {"id": "d", "text": "6 years"}], "correct": "b", "explanation": "The Lok Sabha term is 5 years unless dissolved earlier.", "difficulty": "easy"},
            {"text": "The term of Rajya Sabha members is:", "options": [{"id": "a", "text": "5 years"}, {"id": "b", "text": "6 years"}, {"id": "c", "text": "4 years"}, {"id": "d", "text": "3 years"}], "correct": "b", "explanation": "Rajya Sabha members serve for 6 years, with 1/3 retiring every 2 years.", "difficulty": "medium"},
            {"text": "Who is the Chairman of Rajya Sabha?", "options": [{"id": "a", "text": "Prime Minister"}, {"id": "b", "text": "Vice President"}, {"id": "c", "text": "President"}, {"id": "d", "text": "Speaker"}], "correct": "b", "explanation": "The Vice President of India is the ex-officio Chairman of Rajya Sabha.", "difficulty": "easy"},
        ],

        # UPSC Geography - Chapter 0: Physical Geography
        (exams[0], subjects[exams[0]][2], 0): [
            {"text": "Which is the longest mountain range in India?", "options": [{"id": "a", "text": "Western Ghats"}, {"id": "b", "text": "Eastern Ghats"}, {"id": "c", "text": "Himalayas"}, {"id": "d", "text": "Satpura"}], "correct": "c", "explanation": "The Himalayas is the longest mountain range in India.", "difficulty": "easy"},
            {"text": "The climate of India is primarily:", "options": [{"id": "a", "text": "Tropical"}, {"id": "b", "text": "Subtropical"}, {"id": "c", "text": "Temperate"}, {"id": "d", "text": "Monsoon"}], "correct": "d", "explanation": "India's climate is dominated by the monsoon system.", "difficulty": "medium"},
            {"text": "Which plateau is known as the 'Roof of the World'?", "options": [{"id": "a", "text": "Deccan Plateau"}, {"id": "b", "text": "Tibetan Plateau"}, {"id": "c", "text": "Malwa Plateau"}, {"id": "d", "text": "Chhota Nagpur Plateau"}], "correct": "b", "explanation": "The Tibetan Plateau is often called the 'Roof of the World'.", "difficulty": "medium"},
            {"text": "The Western Ghats run parallel to:", "options": [{"id": "a", "text": "Eastern coast"}, {"id": "b", "text": "Western coast"}, {"id": "c", "text": "Northern coast"}, {"id": "d", "text": "Southern coast"}], "correct": "b", "explanation": "The Western Ghats run along the western coast of India.", "difficulty": "easy"},
            {"text": "Which river is the longest in India?", "options": [{"id": "a", "text": "Brahmaputra"}, {"id": "b", "text": "Ganges"}, {"id": "c", "text": "Indus"}, {"id": "d", "text": "Yamuna"}], "correct": "b", "explanation": "The Ganges (Ganga) is the longest river in India, flowing for 2525 km.", "difficulty": "easy"},
        ],
        # UPSC Geography - Chapter 1: Human Geography
        (exams[0], subjects[exams[0]][2], 1): [
            {"text": "India's population according to 2021 Census is approximately:", "options": [{"id": "a", "text": "1.35 billion"}, {"id": "b", "text": "1.40 billion"}, {"id": "c", "text": "1.45 billion"}, {"id": "d", "text": "1.30 billion"}], "correct": "b", "explanation": "India's population in 2021 Census was approximately 1.40 billion.", "difficulty": "medium"},
            {"text": "Which is the most densely populated state in India?", "options": [{"id": "a", "text": "Rajasthan"}, {"id": "b", "text": "Delhi"}, {"id": "c", "text": "Karnataka"}, {"id": "d", "text": "Maharashtra"}], "correct": "b", "explanation": "Delhi has the highest population density among Indian states/UTs.", "difficulty": "medium"},
            {"text": "The urbanization rate in India is:", "options": [{"id": "a", "text": "Around 35%"}, {"id": "b", "text": "Around 40%"}, {"id": "c", "text": "Around 50%"}, {"id": "d", "text": "Around 25%"}], "correct": "a", "explanation": "Around 35% of India's population lives in urban areas (2021 Census).", "difficulty": "medium"},
            {"text": "Which city is the largest by population in India?", "options": [{"id": "a", "text": "Delhi"}, {"id": "b", "text": "Mumbai"}, {"id": "c", "text": "Bangalore"}, {"id": "d", "text": "Hyderabad"}], "correct": "b", "explanation": "Mumbai is the largest city in India by population.", "difficulty": "easy"},
            {"text": "The literacy rate in India as per 2021 Census is:", "options": [{"id": "a", "text": "Around 70%"}, {"id": "b", "text": "Around 75%"}, {"id": "c", "text": "Around 80%"}, {"id": "d", "text": "Around 65%"}], "correct": "b", "explanation": "India's literacy rate in 2021 Census is approximately 74.7%.", "difficulty": "hard"},
        ],
        # UPSC Geography - Chapter 2: Biogeography
        (exams[0], subjects[exams[0]][2], 2): [
            {"text": "India is home to approximately what percentage of world's biodiversity?", "options": [{"id": "a", "text": "5%"}, {"id": "b", "text": "8%"}, {"id": "c", "text": "12%"}, {"id": "d", "text": "15%"}], "correct": "b", "explanation": "India accounts for about 8% of the world's biodiversity.", "difficulty": "medium"},
            {"text": "Which is NOT one of India's biodiversity hotspots?", "options": [{"id": "a", "text": "Western Ghats"}, {"id": "b", "text": "Himalayas"}, {"id": "c", "text": "Indo-Burma"}, {"id": "d", "text": "Deccan Plateau"}], "correct": "d", "explanation": "India has 4 biodiversity hotspots: Western Ghats, Himalayas, Indo-Burma, Sundarbans.", "difficulty": "hard"},
            {"text": "Tiger conservation project in India is called:", "options": [{"id": "a", "text": "Project Elephant"}, {"id": "b", "text": "Project Tiger"}, {"id": "c", "text": "Project Leopard"}, {"id": "d", "text": "Project Rhino"}], "correct": "b", "explanation": "Project Tiger was launched in 1973 to conserve wild tigers in India.", "difficulty": "easy"},
            {"text": "Which animal is endemic to Western Ghats?", "options": [{"id": "a", "text": "Asian Elephant"}, {"id": "b", "text": "Nilgiri Tahr"}, {"id": "c", "text": "Bengal Tiger"}, {"id": "d", "text": "Indian Rhinoceros"}], "correct": "b", "explanation": "Nilgiri Tahr is endemic to the Western Ghats.", "difficulty": "hard"},
            {"text": "The Sundarbans is known for:", "options": [{"id": "a", "text": "Tigers"}, {"id": "b", "text": "Mangrove forests"}, {"id": "c", "text": "Both tigers and mangroves"}, {"id": "d", "text": "Coral reefs"}], "correct": "c", "explanation": "Sundarbans is famous for mangrove forests and Bengal tigers.", "difficulty": "easy"},
        ],

        # UPSC Economy - Chapter 0: Microeconomics
        (exams[0], subjects[exams[0]][3], 0): [
            {"text": "Microeconomics deals with:", "options": [{"id": "a", "text": "Economy as a whole"}, {"id": "b", "text": "Individual markets and firms"}, {"id": "c", "text": "International trade"}, {"id": "d", "text": "Government policies"}], "correct": "b", "explanation": "Microeconomics studies individual markets, firms, and consumer behavior.", "difficulty": "easy"},
            {"text": "The law of demand states that:", "options": [{"id": "a", "text": "As price increases, quantity demanded increases"}, {"id": "b", "text": "As price decreases, quantity demanded increases"}, {"id": "c", "text": "Price and demand are unrelated"}, {"id": "d", "text": "Supply determines demand"}], "correct": "b", "explanation": "Law of demand: inverse relationship between price and quantity demanded.", "difficulty": "easy"},
            {"text": "Elasticity of demand measures:", "options": [{"id": "a", "text": "Change in price"}, {"id": "b", "text": "Change in supply"}, {"id": "c", "text": "Responsiveness of quantity demanded to price change"}, {"id": "d", "text": "Production capacity"}], "correct": "c", "explanation": "Elasticity measures how responsive demand is to price changes.", "difficulty": "medium"},
            {"text": "A perfectly competitive market has:", "options": [{"id": "a", "text": "One seller"}, {"id": "b", "text": "Few sellers"}, {"id": "c", "text": "Many sellers with identical products"}, {"id": "d", "text": "Controlled prices"}], "correct": "c", "explanation": "Perfect competition has many firms selling identical, homogeneous products.", "difficulty": "medium"},
            {"text": "Consumer surplus is:", "options": [{"id": "a", "text": "Price paid minus quantity"}, {"id": "b", "text": "Difference between willingness to pay and actual price"}, {"id": "c", "text": "Extra money in consumer's pocket"}, {"id": "d", "text": "Excess supply"}], "correct": "b", "explanation": "Consumer surplus is the difference between what consumers are willing to pay and what they actually pay.", "difficulty": "hard"},
        ],
        # UPSC Economy - Chapter 1: Macroeconomics
        (exams[0], subjects[exams[0]][3], 1): [
            {"text": "Macroeconomics deals with:", "options": [{"id": "a", "text": "Individual firms"}, {"id": "b", "text": "The economy as a whole"}, {"id": "c", "text": "Personal finance"}, {"id": "d", "text": "Stock markets"}], "correct": "b", "explanation": "Macroeconomics studies the economy as a whole, including GDP, inflation, employment.", "difficulty": "easy"},
            {"text": "GDP stands for:", "options": [{"id": "a", "text": "Government Development Product"}, {"id": "b", "text": "Gross Domestic Product"}, {"id": "c", "text": "Global Development Plan"}, {"id": "d", "text": "General Distribution of Production"}], "correct": "b", "explanation": "GDP (Gross Domestic Product) is the total value of goods and services produced.", "difficulty": "easy"},
            {"text": "Inflation is:", "options": [{"id": "a", "text": "Decrease in prices"}, {"id": "b", "text": "Increase in general price level"}, {"id": "c", "text": "Increase in GDP"}, {"id": "d", "text": "Increase in unemployment"}], "correct": "b", "explanation": "Inflation is a persistent increase in the general price level of goods and services.", "difficulty": "easy"},
            {"text": "The main objective of monetary policy is:", "options": [{"id": "a", "text": "Increase taxes"}, {"id": "b", "text": "Control inflation and promote growth"}, {"id": "c", "text": "Increase government spending"}, {"id": "d", "text": "Reduce imports"}], "correct": "b", "explanation": "Monetary policy aims to control inflation, promote growth, and maintain price stability.", "difficulty": "medium"},
            {"text": "Unemployment rate measures:", "options": [{"id": "a", "text": "People without jobs"}, {"id": "b", "text": "Percentage of labor force without jobs"}, {"id": "c", "text": "Total jobs available"}, {"id": "d", "text": "Job creation rate"}], "correct": "b", "explanation": "Unemployment rate is the percentage of the labor force that is jobless.", "difficulty": "medium"},
        ],
        # UPSC Economy - Chapter 2: International Trade
        (exams[0], subjects[exams[0]][3], 2): [
            {"text": "Comparative advantage in trade refers to:", "options": [{"id": "a", "text": "Having lower costs in all products"}, {"id": "b", "text": "Ability to produce at lower opportunity cost"}, {"id": "c", "text": "Having more resources"}, {"id": "d", "text": "Being geographically closer"}], "correct": "b", "explanation": "Comparative advantage is producing a good at a lower opportunity cost than others.", "difficulty": "hard"},
            {"text": "Tariffs are taxes on:", "options": [{"id": "a", "text": "Income"}, {"id": "b", "text": "Imported goods"}, {"id": "c", "text": "Production"}, {"id": "d", "text": "Employment"}], "correct": "b", "explanation": "Tariffs are taxes imposed on imported goods to protect domestic industries.", "difficulty": "easy"},
            {"text": "Trade deficit means:", "options": [{"id": "a", "text": "More exports than imports"}, {"id": "b", "text": "Equal exports and imports"}, {"id": "c", "text": "More imports than exports"}, {"id": "d", "text": "No international trade"}], "correct": "c", "explanation": "Trade deficit occurs when imports exceed exports.", "difficulty": "medium"},
            {"text": "WTO stands for:", "options": [{"id": "a", "text": "World Trade Organization"}, {"id": "b", "text": "World Training Office"}, {"id": "c", "text": "Worldwide Trade Opportunities"}, {"id": "d", "text": "Western Trade Operation"}], "correct": "a", "explanation": "WTO (World Trade Organization) regulates international trade between nations.", "difficulty": "easy"},
            {"text": "Foreign Direct Investment (FDI) is:", "options": [{"id": "a", "text": "Short-term investment in stocks"}, {"id": "b", "text": "Long-term investment in producing assets abroad"}, {"id": "c", "text": "Government loans"}, {"id": "d", "text": "Remittances from workers"}], "correct": "b", "explanation": "FDI is long-term investment in productive assets like factories abroad.", "difficulty": "medium"},
        ],

        # JEE Mathematics - Chapter 0: Limits
        (exams[1], subjects[exams[1]][0], 0): [
            {"text": "lim(x→0) sin(x)/x = ?", "options": [{"id": "a", "text": "0"}, {"id": "b", "text": "∞"}, {"id": "c", "text": "1"}, {"id": "d", "text": "undefined"}], "correct": "c", "explanation": "Standard limit: lim(x→0) sin(x)/x = 1", "difficulty": "easy"},
            {"text": "lim(x→∞) (1 + 1/x)^x = ?", "options": [{"id": "a", "text": "1"}, {"id": "b", "text": "e"}, {"id": "c", "text": "0"}, {"id": "d", "text": "∞"}], "correct": "b", "explanation": "This is Euler's number e ≈ 2.71828", "difficulty": "medium"},
            {"text": "lim(x→0) (e^x - 1)/x = ?", "options": [{"id": "a", "text": "0"}, {"id": "b", "text": "e"}, {"id": "c", "text": "1"}, {"id": "d", "text": "e-1"}], "correct": "c", "explanation": "Using Taylor series or L'Hôpital's rule, this equals 1", "difficulty": "medium"},
            {"text": "A function is continuous at x=a if:", "options": [{"id": "a", "text": "f(a) is defined"}, {"id": "b", "text": "lim(x→a) f(x) exists"}, {"id": "c", "text": "lim(x→a) f(x) = f(a)"}, {"id": "d", "text": "f'(a) exists"}], "correct": "c", "explanation": "Continuity requires the limit equals the function value", "difficulty": "easy"},
            {"text": "lim(x→2) (x^2 - 4)/(x - 2) = ?", "options": [{"id": "a", "text": "0"}, {"id": "b", "text": "2"}, {"id": "c", "text": "4"}, {"id": "d", "text": "∞"}], "correct": "c", "explanation": "(x^2-4)/(x-2) = (x+2)(x-2)/(x-2) = x+2, limit is 4", "difficulty": "medium"},
        ],
        # JEE Mathematics - Chapter 1: Differentiation
        (exams[1], subjects[exams[1]][0], 1): [
            {"text": "d/dx (x^n) = ?", "options": [{"id": "a", "text": "x^(n-1)"}, {"id": "b", "text": "nx^(n-1)"}, {"id": "c", "text": "nx^n"}, {"id": "d", "text": "n/x"}], "correct": "b", "explanation": "Power rule: d/dx (x^n) = nx^(n-1)", "difficulty": "easy"},
            {"text": "d/dx (sin x) = ?", "options": [{"id": "a", "text": "cos x"}, {"id": "b", "text": "-cos x"}, {"id": "c", "text": "sin x"}, {"id": "d", "text": "-sin x"}], "correct": "a", "explanation": "Derivative of sin x is cos x", "difficulty": "easy"},
            {"text": "d/dx (e^x) = ?", "options": [{"id": "a", "text": "e^x"}, {"id": "b", "text": "1"}, {"id": "c", "text": "0"}, {"id": "d", "text": "x*e^x"}], "correct": "a", "explanation": "Derivative of e^x is e^x itself", "difficulty": "easy"},
            {"text": "Using product rule, d/dx (uv) = ?", "options": [{"id": "a", "text": "u'v + uv'"}, {"id": "b", "text": "u'v'"}, {"id": "c", "text": "uv' - u'v"}, {"id": "d", "text": "(u+v)'"}], "correct": "a", "explanation": "Product rule: d/dx (uv) = u'v + uv'", "difficulty": "medium"},
            {"text": "If f(x) = x^3 - 2x + 5, then f'(x) = ?", "options": [{"id": "a", "text": "3x^2 - 2"}, {"id": "b", "text": "3x - 2"}, {"id": "c", "text": "x^2 - 2"}, {"id": "d", "text": "3x^3 - 2"}], "correct": "a", "explanation": "f'(x) = 3x^2 - 2 using power rule", "difficulty": "medium"},
        ],
        # JEE Mathematics - Chapter 2: Integration
        (exams[1], subjects[exams[1]][0], 2): [
            {"text": "∫ x^n dx = ?", "options": [{"id": "a", "text": "x^(n+1)/(n+1) + C"}, {"id": "b", "text": "nx^(n-1) + C"}, {"id": "c", "text": "x^(n+1) + C"}, {"id": "d", "text": "n*x + C"}], "correct": "a", "explanation": "Power rule for integration: ∫ x^n dx = x^(n+1)/(n+1) + C", "difficulty": "easy"},
            {"text": "∫ sin x dx = ?", "options": [{"id": "a", "text": "cos x + C"}, {"id": "b", "text": "-cos x + C"}, {"id": "c", "text": "sin x + C"}, {"id": "d", "text": "-sin x + C"}], "correct": "b", "explanation": "∫ sin x dx = -cos x + C", "difficulty": "easy"},
            {"text": "∫ e^x dx = ?", "options": [{"id": "a", "text": "e^x + C"}, {"id": "b", "text": "1 + C"}, {"id": "c", "text": "x*e^x + C"}, {"id": "d", "text": "e^(x+1) + C"}], "correct": "a", "explanation": "∫ e^x dx = e^x + C", "difficulty": "easy"},
            {"text": "∫₀¹ x dx = ?", "options": [{"id": "a", "text": "0"}, {"id": "b", "text": "0.5"}, {"id": "c", "text": "1"}, {"id": "d", "text": "∞"}], "correct": "b", "explanation": "∫₀¹ x dx = [x²/2]₀¹ = 1/2 = 0.5", "difficulty": "medium"},
            {"text": "∫ 1/x dx = ?", "options": [{"id": "a", "text": "ln|x| + C"}, {"id": "b", "text": "-1/x^2 + C"}, {"id": "c", "text": "ln x + C"}, {"id": "d", "text": "1/x^2 + C"}], "correct": "a", "explanation": "∫ 1/x dx = ln|x| + C", "difficulty": "medium"},
        ],

        # JEE Physics - Chapter 0: Kinematics
        (exams[1], subjects[exams[1]][1], 0): [
            {"text": "Velocity is:", "options": [{"id": "a", "text": "Distance/time"}, {"id": "b", "text": "Displacement/time"}, {"id": "c", "text": "Speed with direction"}, {"id": "d", "text": "Change in speed"}], "correct": "c", "explanation": "Velocity is speed with direction (vector quantity)", "difficulty": "easy"},
            {"text": "For uniform acceleration, v = u + at. Here 'a' is:", "options": [{"id": "a", "text": "Acceleration"}, {"id": "b", "text": "Distance"}, {"id": "c", "text": "Time"}, {"id": "d", "text": "Final velocity"}], "correct": "a", "explanation": "This is the first equation of motion; a is acceleration", "difficulty": "easy"},
            {"text": "Projectile motion components are:", "options": [{"id": "a", "text": "Horizontal and vertical"}, {"id": "b", "text": "Parallel and perpendicular"}, {"id": "c", "text": "Radial and tangential"}, {"id": "d", "text": "Angular and linear"}], "correct": "a", "explanation": "Projectile motion is analyzed as horizontal and vertical components", "difficulty": "medium"},
            {"text": "At maximum height of projectile, vertical velocity is:", "options": [{"id": "a", "text": "Maximum"}, {"id": "b", "text": "Zero"}, {"id": "c", "text": "Equal to horizontal velocity"}, {"id": "d", "text": "Minimum"}], "correct": "b", "explanation": "At max height, vertical velocity = 0", "difficulty": "easy"},
            {"text": "Time to reach max height if u = 20 m/s, g = 10 m/s²:", "options": [{"id": "a", "text": "1 second"}, {"id": "b", "text": "2 seconds"}, {"id": "c", "text": "3 seconds"}, {"id": "d", "text": "4 seconds"}], "correct": "b", "explanation": "t = u/g = 20/10 = 2 seconds", "difficulty": "medium"},
        ],
        # JEE Physics - Chapter 1: Laws of Motion
        (exams[1], subjects[exams[1]][1], 1): [
            {"text": "Newton's First Law states:", "options": [{"id": "a", "text": "F = ma"}, {"id": "b", "text": "Object at rest stays at rest unless force acts"}, {"id": "c", "text": "Action = Reaction"}, {"id": "d", "text": "Momentum is conserved"}], "correct": "b", "explanation": "First Law: object at rest or motion stays same unless external force acts", "difficulty": "easy"},
            {"text": "Newton's Second Law: F = ma means:", "options": [{"id": "a", "text": "Force is proportional to mass"}, {"id": "b", "text": "Force equals mass times acceleration"}, {"id": "c", "text": "Acceleration is proportional to mass"}, {"id": "d", "text": "Mass equals force"}], "correct": "b", "explanation": "F = ma: Force = mass × acceleration", "difficulty": "easy"},
            {"text": "Newton's Third Law:", "options": [{"id": "a", "text": "Action and reaction are equal and opposite"}, {"id": "b", "text": "Energy is conserved"}, {"id": "c", "text": "Force increases acceleration"}, {"id": "d", "text": "Objects move at constant velocity"}], "correct": "a", "explanation": "Third Law: For every action, there's equal and opposite reaction", "difficulty": "easy"},
            {"text": "If mass = 5 kg and F = 20 N, acceleration = ?", "options": [{"id": "a", "text": "4 m/s²"}, {"id": "b", "text": "5 m/s²"}, {"id": "c", "text": "100 m/s²"}, {"id": "d", "text": "0.25 m/s²"}], "correct": "a", "explanation": "a = F/m = 20/5 = 4 m/s²", "difficulty": "medium"},
            {"text": "Friction force acts:", "options": [{"id": "a", "text": "In the direction of motion"}, {"id": "b", "text": "Opposite to motion"}, {"id": "c", "text": "Perpendicular to surface"}, {"id": "d", "text": "Downward only"}], "correct": "b", "explanation": "Friction opposes the direction of motion", "difficulty": "easy"},
        ],
        # JEE Physics - Chapter 2: Work Energy Power
        (exams[1], subjects[exams[1]][1], 2): [
            {"text": "Work = ?", "options": [{"id": "a", "text": "Force × displacement"}, {"id": "b", "text": "Force × time"}, {"id": "c", "text": "Force × velocity"}, {"id": "d", "text": "Mass × acceleration"}], "correct": "a", "explanation": "Work = Force × displacement × cos(θ)", "difficulty": "easy"},
            {"text": "Kinetic Energy = ?", "options": [{"id": "a", "text": "mgh"}, {"id": "b", "text": "1/2 mv²"}, {"id": "c", "text": "Fv"}, {"id": "d", "text": "mgh + 1/2 mv²"}], "correct": "b", "explanation": "Kinetic Energy = 1/2 × mass × velocity²", "difficulty": "easy"},
            {"text": "Potential Energy = ?", "options": [{"id": "a", "text": "1/2 mv²"}, {"id": "b", "text": "mgh"}, {"id": "c", "text": "F × d"}, {"id": "d", "text": "Fv"}], "correct": "b", "explanation": "Potential Energy (gravitational) = mass × g × height", "difficulty": "easy"},
            {"text": "Power is:", "options": [{"id": "a", "text": "Work/time"}, {"id": "b", "text": "Force × velocity"}, {"id": "c", "text": "Energy/time"}, {"id": "d", "text": "All of above"}], "correct": "d", "explanation": "Power = Work/time = Energy/time = Force × velocity", "difficulty": "hard"},
            {"text": "1 Watt equals:", "options": [{"id": "a", "text": "1 J/s"}, {"id": "b", "text": "1 N·m"}, {"id": "c", "text": "1 kg·m²/s"}, {"id": "d", "text": "1 J"}], "correct": "a", "explanation": "1 Watt = 1 Joule/second", "difficulty": "medium"},
        ],

        # JEE Chemistry - Chapter 0: Atomic Structure
        (exams[1], subjects[exams[1]][2], 0): [
            {"text": "Who discovered the electron?", "options": [{"id": "a", "text": "Dalton"}, {"id": "b", "text": "Bohr"}, {"id": "c", "text": "Thomson"}, {"id": "d", "text": "Rutherford"}], "correct": "c", "explanation": "J.J. Thomson discovered the electron in 1897", "difficulty": "easy"},
            {"text": "Bohr's model proposed that electrons:", "options": [{"id": "a", "text": "Orbit in specific energy levels"}, {"id": "b", "text": "Are randomly distributed"}, {"id": "c", "text": "Cannot be located"}, {"id": "d", "text": "Are in clouds"}], "correct": "a", "explanation": "Bohr proposed electrons orbit in fixed energy levels", "difficulty": "medium"},
            {"text": "What are the 4 quantum numbers?", "options": [{"id": "a", "text": "n, l, m, s"}, {"id": "b", "text": "p, d, f, s"}, {"id": "c", "text": "x, y, z, t"}, {"id": "d", "text": "a, b, c, d"}], "correct": "a", "explanation": "Principal (n), azimuthal (l), magnetic (m), spin (s)", "difficulty": "hard"},
            {"text": "Maximum electrons in s orbital:", "options": [{"id": "a", "text": "2"}, {"id": "b", "text": "4"}, {"id": "c", "text": "6"}, {"id": "d", "text": "10"}], "correct": "a", "explanation": "s orbital can hold maximum 2 electrons", "difficulty": "easy"},
            {"text": "Aufbau principle states:", "options": [{"id": "a", "text": "Electrons fill orbitals randomly"}, {"id": "b", "text": "Electrons fill lowest energy orbitals first"}, {"id": "c", "text": "All orbitals fill simultaneously"}, {"id": "d", "text": "Electrons avoid orbitals"}], "correct": "b", "explanation": "Aufbau: electrons fill lowest energy orbitals first", "difficulty": "medium"},
        ],
        # JEE Chemistry - Chapter 1: Chemical Bonding
        (exams[1], subjects[exams[1]][2], 1): [
            {"text": "Ionic bond forms between:", "options": [{"id": "a", "text": "Two metals"}, {"id": "b", "text": "Two nonmetals"}, {"id": "c", "text": "Metal and nonmetal"}, {"id": "d", "text": "Same element"}], "correct": "c", "explanation": "Ionic bond forms between metal (loses electrons) and nonmetal (gains electrons)", "difficulty": "easy"},
            {"text": "Covalent bond involves:", "options": [{"id": "a", "text": "Transfer of electrons"}, {"id": "b", "text": "Sharing of electrons"}, {"id": "c", "text": "Loss of electrons"}, {"id": "d", "text": "Gain of electrons"}], "correct": "b", "explanation": "Covalent bond: electrons are shared between atoms", "difficulty": "easy"},
            {"text": "Coordinate covalent bond is:", "options": [{"id": "a", "text": "Bond from both atoms equally"}, {"id": "b", "text": "Bond where both electrons from one atom"}, {"id": "c", "text": "No bond"}, {"id": "d", "text": "Metallic bond"}], "correct": "b", "explanation": "Coordinate bond: both electrons come from one atom (donor)", "difficulty": "hard"},
            {"text": "Hydrogen bonding occurs between:", "options": [{"id": "a", "text": "Any two atoms"}, {"id": "b", "text": "H and highly electronegative atoms (N,O,F)"}, {"id": "c", "text": "Two hydrogen atoms"}, {"id": "d", "text": "Metals only"}], "correct": "b", "explanation": "H-bonding: between H and N, O, or F", "difficulty": "medium"},
            {"text": "Electronegativity is the ability of atom to:", "options": [{"id": "a", "text": "Lose electrons"}, {"id": "b", "text": "Gain electrons"}, {"id": "c", "text": "Attract electrons"}, {"id": "d", "text": "Share electrons"}], "correct": "c", "explanation": "Electronegativity: ability to attract electrons in a bond", "difficulty": "medium"},
        ],
        # JEE Chemistry - Chapter 2: Periodic Table
        (exams[1], subjects[exams[1]][2], 2): [
            {"text": "Who arranged the periodic table?", "options": [{"id": "a", "text": "Dalton"}, {"id": "b", "text": "Mendeleev"}, {"id": "c", "text": "Boyle"}, {"id": "d", "text": "Lavoisier"}], "correct": "b", "explanation": "Dmitri Mendeleev created the periodic table in 1869", "difficulty": "easy"},
            {"text": "Elements in same column have:", "options": [{"id": "a", "text": "Same atomic number"}, {"id": "b", "text": "Same valence electrons"}, {"id": "c", "text": "Same mass"}, {"id": "d", "text": "Same properties always"}], "correct": "b", "explanation": "Elements in same group (column) have same number of valence electrons", "difficulty": "medium"},
            {"text": "Atomic size generally increases:", "options": [{"id": "a", "text": "Left to right in a period"}, {"id": "b", "text": "Down a group"}, {"id": "c", "text": "From transition metals"}, {"id": "d", "text": "With increasing atomic number always"}], "correct": "b", "explanation": "Atomic size increases down a group (more electron shells)", "difficulty": "medium"},
            {"text": "Ionization energy is:", "options": [{"id": "a", "text": "Energy gained by electron"}, {"id": "b", "text": "Energy needed to remove electron"}, {"id": "c", "text": "Energy released in bonding"}, {"id": "d", "text": "Energy in nucleus"}], "correct": "b", "explanation": "Ionization energy: energy required to remove 1 electron from atom", "difficulty": "medium"},
            {"text": "Noble gases are unreactive because:", "options": [{"id": "a", "text": "They have no electrons"}, {"id": "b", "text": "They have full valence shell"}, {"id": "c", "text": "They are too heavy"}, {"id": "d", "text": "They don't exist"}], "correct": "b", "explanation": "Noble gases have complete valence electron shells (very stable)", "difficulty": "easy"},
        ],

        # NEET Biology - Chapter 0: Cell Biology
        (exams[2], subjects[exams[2]][0], 0): [
            {"text": "Cell theory states:", "options": [{"id": "a", "text": "All organisms made of cells"}, {"id": "b", "text": "Cells come from pre-existing cells"}, {"id": "c", "text": "Cell is basic unit of life"}, {"id": "d", "text": "All of above"}], "correct": "d", "explanation": "Cell theory: All three statements are true", "difficulty": "medium"},
            {"text": "Prokaryotic cells lack:", "options": [{"id": "a", "text": "Cell membrane"}, {"id": "b", "text": "Nucleus"}, {"id": "c", "text": "Cytoplasm"}, {"id": "d", "text": "Ribosomes"}], "correct": "b", "explanation": "Prokaryotes (bacteria, archaea) have no membrane-bound nucleus", "difficulty": "easy"},
            {"text": "Which organelle produces ATP?", "options": [{"id": "a", "text": "Ribosome"}, {"id": "b", "text": "Mitochondria"}, {"id": "c", "text": "Golgi apparatus"}, {"id": "d", "text": "Lysosome"}], "correct": "b", "explanation": "Mitochondria: 'powerhouse of the cell', produces ATP", "difficulty": "easy"},
            {"text": "Cell wall is present in:", "options": [{"id": "a", "text": "Animal cells only"}, {"id": "b", "text": "Plant cells only"}, {"id": "c", "text": "Both equally"}, {"id": "d", "text": "Viruses"}], "correct": "b", "explanation": "Cell wall is in plant cells (cellulose) and bacteria (peptidoglycan)", "difficulty": "easy"},
            {"text": "Plant cells have but animal cells don't:", "options": [{"id": "a", "text": "Mitochondria"}, {"id": "b", "text": "Cell wall and chloroplasts"}, {"id": "c", "text": "Ribosomes"}, {"id": "d", "text": "Nucleus"}], "correct": "b", "explanation": "Plant-specific: cell wall (cellulose) and chloroplasts", "difficulty": "easy"},
        ],
        # NEET Biology - Chapter 1: Genetics
        (exams[2], subjects[exams[2]][0], 1): [
            {"text": "Mendel's First Law is:", "options": [{"id": "a", "text": "Law of Segregation"}, {"id": "b", "text": "Law of Independent Assortment"}, {"id": "c", "text": "Law of Dominance"}, {"id": "d", "text": "Law of Inheritance"}], "correct": "a", "explanation": "Law of Segregation: traits segregate in equal proportions", "difficulty": "medium"},
            {"text": "DNA stands for:", "options": [{"id": "a", "text": "Diribonucleic Acid"}, {"id": "b", "text": "Deoxyribonucleic Acid"}, {"id": "c", "text": "Dinucleic Acid"}, {"id": "d", "text": "Diribose Nucleic Acid"}], "correct": "b", "explanation": "DNA = Deoxyribonucleic Acid, contains deoxyribose sugar", "difficulty": "easy"},
            {"text": "Bases in DNA pair as:", "options": [{"id": "a", "text": "A-C, G-T"}, {"id": "b", "text": "A-T, G-C"}, {"id": "c", "text": "A-G, C-T"}, {"id": "d", "text": "Any with any"}], "correct": "b", "explanation": "Chargaff's rule: A-T (2 bonds), G-C (3 bonds)", "difficulty": "easy"},
            {"text": "Dominant trait is:", "options": [{"id": "a", "text": "Always expressed"}, {"id": "b", "text": "Expressed in heterozygote"}, {"id": "c", "text": "Hidden in homozygote"}, {"id": "d", "text": "More common"}], "correct": "b", "explanation": "Dominant trait expressed in heterozygous individuals", "difficulty": "medium"},
            {"text": "Genotype is:", "options": [{"id": "a", "text": "Physical appearance"}, {"id": "b", "text": "Genetic makeup"}, {"id": "c", "text": "Observable traits"}, {"id": "d", "text": "Protein structure"}], "correct": "b", "explanation": "Genotype: genetic composition of organism", "difficulty": "easy"},
        ],
        # NEET Biology - Chapter 2: Ecology
        (exams[2], subjects[exams[2]][0], 2): [
            {"text": "Ecosystem includes:", "options": [{"id": "a", "text": "Only plants"}, {"id": "b", "text": "Living and non-living components"}, {"id": "c", "text": "Only animals"}, {"id": "d", "text": "Soil only"}], "correct": "b", "explanation": "Ecosystem: biotic (organisms) + abiotic (soil, climate, water)", "difficulty": "easy"},
            {"text": "Primary producer in food chain:", "options": [{"id": "a", "text": "Herbivore"}, {"id": "b", "text": "Carnivore"}, {"id": "c", "text": "Plant/Autotroph"}, {"id": "d", "text": "Decomposer"}], "correct": "c", "explanation": "Producers (plants) convert solar energy to chemical energy", "difficulty": "easy"},
            {"text": "Biodiversity refers to:", "options": [{"id": "a", "text": "Number of species"}, {"id": "b", "text": "Genetic variation"}, {"id": "c", "text": "Ecosystem variety"}, {"id": "d", "text": "All of above"}], "correct": "d", "explanation": "Biodiversity: species, genetic, and ecosystem diversity", "difficulty": "medium"},
            {"text": "Decomposer organisms include:", "options": [{"id": "a", "text": "Herbivores"}, {"id": "b", "text": "Bacteria and fungi"}, {"id": "c", "text": "Carnivores"}, {"id": "d", "text": "Plants"}], "correct": "b", "explanation": "Decomposers: bacteria, fungi break down dead matter", "difficulty": "easy"},
            {"text": "Succession is:", "options": [{"id": "a", "text": "Seasonal change"}, {"id": "b", "text": "Gradual change in species composition"}, {"id": "c", "text": "Extinction event"}, {"id": "d", "text": "Migration of animals"}], "correct": "b", "explanation": "Ecological succession: gradual change in community over time", "difficulty": "medium"},
        ],

        # NEET Physics - Chapter 0: Mechanics
        (exams[2], subjects[exams[2]][1], 0): [
            {"text": "Scalar quantity is:", "options": [{"id": "a", "text": "Has magnitude and direction"}, {"id": "b", "text": "Only magnitude"}, {"id": "c", "text": "Only direction"}, {"id": "d", "text": "Can be negative only"}], "correct": "b", "explanation": "Scalar: only magnitude (e.g., speed, mass, temperature)", "difficulty": "easy"},
            {"text": "Vector quantity is:", "options": [{"id": "a", "text": "Speed"}, {"id": "b", "text": "Temperature"}, {"id": "c", "text": "Velocity"}, {"id": "d", "text": "Mass"}], "correct": "c", "explanation": "Velocity: magnitude + direction (vector)", "difficulty": "easy"},
            {"text": "Acceleration of free fall (g) is:", "options": [{"id": "a", "text": "9.8 m/s²"}, {"id": "b", "text": "9.8 ft/s²"}, {"id": "c", "text": "8.9 m/s²"}, {"id": "d", "text": "10.8 m/s²"}], "correct": "a", "explanation": "g ≈ 9.8 m/s² (or 10 m/s² for approximations)", "difficulty": "easy"},
            {"text": "Momentum is defined as:", "options": [{"id": "a", "text": "Mass × velocity"}, {"id": "b", "text": "Force × time"}, {"id": "c", "text": "Both are equal"}, {"id": "d", "text": "Mass/velocity"}], "correct": "c", "explanation": "p = m×v = F×t (impulse-momentum theorem)", "difficulty": "medium"},
            {"text": "Collision where KE is conserved:", "options": [{"id": "a", "text": "Elastic"}, {"id": "b", "text": "Inelastic"}, {"id": "c", "text": "Both"}, {"id": "d", "text": "Neither"}], "correct": "a", "explanation": "Elastic collision: KE conserved; Inelastic: KE not conserved", "difficulty": "medium"},
        ],
        # NEET Physics - Chapter 1: Optics
        (exams[2], subjects[exams[2]][1], 1): [
            {"text": "Speed of light is:", "options": [{"id": "a", "text": "2×10^8 m/s"}, {"id": "b", "text": "3×10^8 m/s"}, {"id": "c", "text": "4×10^8 m/s"}, {"id": "d", "text": "1×10^8 m/s"}], "correct": "b", "explanation": "c = 3×10^8 m/s (approximately)", "difficulty": "easy"},
            {"text": "Convex lens forms:", "options": [{"id": "a", "text": "Real or virtual image"}, {"id": "b", "text": "Only real"}, {"id": "c", "text": "Only virtual"}, {"id": "d", "text": "Magnified only"}], "correct": "a", "explanation": "Convex lens: real image if object beyond focal length, virtual if closer", "difficulty": "medium"},
            {"text": "Focal length of concave mirror:", "options": [{"id": "a", "text": "Positive"}, {"id": "b", "text": "Negative"}, {"id": "c", "text": "Zero"}, {"id": "d", "text": "Infinity"}], "correct": "a", "explanation": "Concave mirror: focal length is positive (real focus)", "difficulty": "hard"},
            {"text": "Refraction occurs when light:", "options": [{"id": "a", "text": "Hits mirror"}, {"id": "b", "text": "Changes medium"}, {"id": "c", "text": "Passes through same medium"}, {"id": "d", "text": "Is absorbed"}], "correct": "b", "explanation": "Refraction: change in direction when light enters different medium", "difficulty": "easy"},
            {"text": "Lens formula is:", "options": [{"id": "a", "text": "1/f = 1/u + 1/v"}, {"id": "b", "text": "f = uv"}, {"id": "c", "text": "v = u + f"}, {"id": "d", "text": "u = v = f"}], "correct": "a", "explanation": "Lens formula: 1/f = 1/u + 1/v (u=object distance, v=image distance)", "difficulty": "hard"},
        ],
        # NEET Physics - Chapter 2: Modern Physics
        (exams[2], subjects[exams[2]][1], 2): [
            {"text": "Photon energy is given by:", "options": [{"id": "a", "text": "hf"}, {"id": "b", "text": "h/f"}, {"id": "c", "text": "h×c"}, {"id": "d", "text": "f/h"}], "correct": "a", "explanation": "E = hf, where h is Planck's constant", "difficulty": "medium"},
            {"text": "Photoelectric effect explains:", "options": [{"id": "a", "text": "Light as wave"}, {"id": "b", "text": "Light as particle (photon)"}, {"id": "c", "text": "Both wave and particle"}, {"id": "d", "text": "Color of light"}], "correct": "b", "explanation": "Photoelectric effect: light acts as particles (photons)", "difficulty": "medium"},
            {"text": "Atomic number is:", "options": [{"id": "a", "text": "Number of neutrons"}, {"id": "b", "text": "Number of protons"}, {"id": "c", "text": "Number of electrons"}, {"id": "d", "text": "Mass of nucleus"}], "correct": "b", "explanation": "Atomic number Z = number of protons (also equals electrons in neutral atom)", "difficulty": "easy"},
            {"text": "Mass number is:", "options": [{"id": "a", "text": "A = protons"}, {"id": "b", "text": "A = electrons"}, {"id": "c", "text": "A = protons + neutrons"}, {"id": "d", "text": "A = protons - neutrons"}], "correct": "c", "explanation": "Mass number A = Z + N (protons + neutrons)", "difficulty": "easy"},
            {"text": "Radioactivity is:", "options": [{"id": "a", "text": "Stable nucleus decay"}, {"id": "b", "text": "Spontaneous nucleus decay"}, {"id": "c", "text": "Artificial process"}, {"id": "d", "text": "Chemical reaction"}], "correct": "b", "explanation": "Radioactivity: spontaneous emission of particles/radiation from nucleus", "difficulty": "medium"},
        ],

        # NEET Chemistry - Chapter 0: Inorganic
        (exams[2], subjects[exams[2]][2], 0): [
            {"text": "Valency is:", "options": [{"id": "a", "text": "Atomic number"}, {"id": "b", "text": "Number of valence electrons"}, {"id": "c", "text": "Combining capacity"}, {"id": "d", "text": "Electron configuration"}], "correct": "c", "explanation": "Valency: combining capacity of element", "difficulty": "medium"},
            {"text": "Acid is a substance that:", "options": [{"id": "a", "text": "Produces OH⁻ ions"}, {"id": "b", "text": "Produces H⁺ ions"}, {"id": "c", "text": "Turns litmus red"}, {"id": "d", "text": "b and c"}], "correct": "d", "explanation": "Acid: produces H⁺ ions (Arrhenius definition); turns litmus red", "difficulty": "easy"},
            {"text": "pH of neutral solution is:", "options": [{"id": "a", "text": "0"}, {"id": "b", "text": "7"}, {"id": "c", "text": "14"}, {"id": "d", "text": "1"}], "correct": "b", "explanation": "pH 7 is neutral (at 25°C); <7 is acidic, >7 is basic", "difficulty": "easy"},
            {"text": "Oxidation involves:", "options": [{"id": "a", "text": "Loss of electrons"}, {"id": "b", "text": "Gain of electrons"}, {"id": "c", "text": "No electron change"}, {"id": "d", "text": "Transfer of protons"}], "correct": "a", "explanation": "Oxidation: loss of electrons; Reduction: gain of electrons", "difficulty": "easy"},
            {"text": "Salt is formed by:", "options": [{"id": "a", "text": "Acid + base"}, {"id": "b", "text": "Acid + water"}, {"id": "c", "text": "Base + water"}, {"id": "d", "text": "Acid + acid"}], "correct": "a", "explanation": "Acid + Base → Salt + Water (neutralization reaction)", "difficulty": "easy"},
        ],
        # NEET Chemistry - Chapter 1: Organic
        (exams[2], subjects[exams[2]][2], 1): [
            {"text": "Organic compounds contain:", "options": [{"id": "a", "text": "Only hydrogen"}, {"id": "b", "text": "Only carbon"}, {"id": "c", "text": "Carbon + H (usually)"}, {"id": "d", "text": "Only nitrogen"}], "correct": "c", "explanation": "Organic compounds: carbon as main element, usually with H, O, N", "difficulty": "easy"},
            {"text": "Alkanes have bonds:", "options": [{"id": "a", "text": "Double"}, {"id": "b", "text": "Single only"}, {"id": "c", "text": "Triple"}, {"id": "d", "text": "Mixed"}], "correct": "b", "explanation": "Alkanes: only single C-C and C-H bonds (CₙH₂ₙ₊₂)", "difficulty": "easy"},
            {"text": "Isomers are:", "options": [{"id": "a", "text": "Different compounds, same formula"}, {"id": "b", "text": "Same compound"}, {"id": "c", "text": "Different formulas"}, {"id": "d", "text": "Polymers"}], "correct": "a", "explanation": "Isomers: same molecular formula, different structures", "difficulty": "medium"},
            {"text": "Functional group in alcohols:", "options": [{"id": "a", "text": "-CHO"}, {"id": "b", "text": "-OH"}, {"id": "c", "text": "-COOH"}, {"id": "d", "text": "-NH₂"}], "correct": "b", "explanation": "Alcohols have -OH (hydroxyl) functional group", "difficulty": "easy"},
            {"text": "Esterification is reaction between:", "options": [{"id": "a", "text": "Acid + acid"}, {"id": "b", "text": "Acid + alcohol"}, {"id": "c", "text": "Base + alcohol"}, {"id": "d", "text": "Alcohol + alcohol"}], "correct": "b", "explanation": "Esterification: Carboxylic acid + Alcohol → Ester + Water", "difficulty": "medium"},
        ],
        # NEET Chemistry - Chapter 2: Physical
        (exams[2], subjects[exams[2]][2], 2): [
            {"text": "Thermodynamics First Law:", "options": [{"id": "a", "text": "Energy conservation"}, {"id": "b", "text": "Entropy increases"}, {"id": "c", "text": "Heat transfer"}, {"id": "d", "text": "All of above"}], "correct": "a", "explanation": "First Law: ΔU = q - w (energy conservation)", "difficulty": "hard"},
            {"text": "Activation energy is:", "options": [{"id": "a", "text": "Energy of products"}, {"id": "b", "text": "Energy needed for reaction to start"}, {"id": "c", "text": "Energy released"}, {"id": "d", "text": "Bond energy"}], "correct": "b", "explanation": "Activation energy: minimum energy needed for reaction", "difficulty": "medium"},
            {"text": "Catalyst:", "options": [{"id": "a", "text": "Increases product"}, {"id": "b", "text": "Increases reaction rate"}, {"id": "c", "text": "Changes equilibrium"}, {"id": "d", "text": "Is consumed"}], "correct": "b", "explanation": "Catalyst: increases reaction rate, not consumed, not in equilibrium", "difficulty": "medium"},
            {"text": "Equilibrium constant K means:", "options": [{"id": "a", "text": "Reaction stops"}, {"id": "b", "text": "Ratio of products to reactants"}, {"id": "c", "text": "No change in concentrations"}, {"id": "d", "text": "b and c"}], "correct": "d", "explanation": "At equilibrium: K = [products]/[reactants]; concentrations stay constant", "difficulty": "hard"},
            {"text": "Le Chatelier's principle:", "options": [{"id": "a", "text": "Equilibrium shifts to minimize change"}, {"id": "b", "text": "System disturbs at equilibrium"}, {"id": "c", "text": "Entropy always increases"}, {"id": "d", "text": "Products always increase"}], "correct": "a", "explanation": "Le Chatelier: system shifts to counteract disturbance", "difficulty": "medium"},
        ],

        # CAT Quant - Chapter 0: Number Systems
        (exams[3], subjects[exams[3]][0], 0): [
            {"text": "LCM of 12, 18 is:", "options": [{"id": "a", "text": "36"}, {"id": "b", "text": "24"}, {"id": "c", "text": "48"}, {"id": "d", "text": "60"}], "correct": "a", "explanation": "12 = 2²×3, 18 = 2×3². LCM = 2²×3² = 36", "difficulty": "medium"},
            {"text": "Prime numbers upto 10:", "options": [{"id": "a", "text": "2,3,5,7"}, {"id": "b", "text": "2,3,5,7,9"}, {"id": "c", "text": "1,2,3,5,7"}, {"id": "d", "text": "3,5,7,9"}], "correct": "a", "explanation": "Prime numbers upto 10: 2,3,5,7", "difficulty": "easy"},
            {"text": "HCF of 24, 36 is:", "options": [{"id": "a", "text": "6"}, {"id": "b", "text": "12"}, {"id": "c", "text": "8"}, {"id": "d", "text": "18"}], "correct": "b", "explanation": "24 = 2³×3, 36 = 2²×3². HCF = 2²×3 = 12", "difficulty": "medium"},
            {"text": "Sum of integers 1 to 100:", "options": [{"id": "a", "text": "5000"}, {"id": "b", "text": "5050"}, {"id": "c", "text": "5100"}, {"id": "d", "text": "5150"}], "correct": "b", "explanation": "Sum = n(n+1)/2 = 100×101/2 = 5050", "difficulty": "medium"},
            {"text": "Which is divisible by 3?", "options": [{"id": "a", "text": "121"}, {"id": "b", "text": "133"}, {"id": "c", "text": "147"}, {"id": "d", "text": "155"}], "correct": "c", "explanation": "147: 1+4+7 = 12 (divisible by 3), so 147 is divisible by 3", "difficulty": "medium"},
        ],
        # CAT Quant - Chapter 1: Percentages
        (exams[3], subjects[exams[3]][0], 1): [
            {"text": "20% of 500 is:", "options": [{"id": "a", "text": "100"}, {"id": "b", "text": "150"}, {"id": "c", "text": "200"}, {"id": "d", "text": "250"}], "correct": "a", "explanation": "20/100 × 500 = 0.2 × 500 = 100", "difficulty": "easy"},
            {"text": "If price increases by 25%, new price is:", "options": [{"id": "a", "text": "125% of original"}, {"id": "b", "text": "25% of original"}, {"id": "c", "text": "75% of original"}, {"id": "d", "text": "225% of original"}], "correct": "a", "explanation": "New price = Original + 25% = 125% of original", "difficulty": "easy"},
            {"text": "Profit% = (SP - CP)/CP × 100. If CP=100, SP=150, profit%:", "options": [{"id": "a", "text": "25%"}, {"id": "b", "text": "50%"}, {"id": "c", "text": "33%"}, {"id": "d", "text": "40%"}], "correct": "b", "explanation": "(150-100)/100 × 100 = 50%", "difficulty": "medium"},
            {"text": "If 30% is removed, what% remains:", "options": [{"id": "a", "text": "30%"}, {"id": "b", "text": "70%"}, {"id": "c", "text": "50%"}, {"id": "d", "text": "60%"}], "correct": "b", "explanation": "Remaining = 100% - 30% = 70%", "difficulty": "easy"},
            {"text": "Successive discounts of 10% and 20%:", "options": [{"id": "a", "text": "30%"}, {"id": "b", "text": "28%"}, {"id": "c", "text": "25%"}, {"id": "d", "text": "32%"}], "correct": "b", "explanation": "After 1st: 90% remains. After 2nd: 90% × 80% = 72% remains, so 28% off", "difficulty": "hard"},
        ],
        # CAT Quant - Chapter 2: Time and Work
        (exams[3], subjects[exams[3]][0], 2): [
            {"text": "If A can do work in 10 days, work per day:", "options": [{"id": "a", "text": "1/5"}, {"id": "b", "text": "1/10"}, {"id": "c", "text": "1/15"}, {"id": "d", "text": "10"}], "correct": "b", "explanation": "Work rate = 1/total time = 1/10 per day", "difficulty": "easy"},
            {"text": "A does work in 6 days, B in 8 days. Together:", "options": [{"id": "a", "text": "14 days"}, {"id": "b", "text": "24/7 days"}, {"id": "c", "text": "3.4 days"}, {"id": "d", "text": "7 days"}], "correct": "c", "explanation": "Combined rate = 1/6 + 1/8 = 7/24, so time = 24/7 ≈ 3.4 days", "difficulty": "hard"},
            {"text": "If work done = rate × time, rate is:", "options": [{"id": "a", "text": "Work/time"}, {"id": "b", "text": "Time/work"}, {"id": "c", "text": "Work × time"}, {"id": "d", "text": "Work + time"}], "correct": "a", "explanation": "Rate = Work/Time (amount of work done per unit time)", "difficulty": "easy"},
            {"text": "A's work in 2 hours + B's work in 3 hours = ?", "options": [{"id": "a", "text": "2A + 3B"}, {"id": "b", "text": "2/A + 3/B"}, {"id": "c", "text": "2(1/A) + 3(1/B)"}, {"id": "d", "text": "A/2 + B/3"}], "correct": "c", "explanation": "Work = rate × time = (1/A) × 2 + (1/B) × 3", "difficulty": "hard"},
            {"text": "Pipe A fills in 6 hrs, B empties in 8 hrs. Together:", "options": [{"id": "a", "text": "24 hours"}, {"id": "b", "text": "14 hours"}, {"id": "c", "text": "1 hour"}, {"id": "d", "text": "2 hours"}], "correct": "a", "explanation": "Net rate = 1/6 - 1/8 = 1/24, so fills in 24 hours", "difficulty": "hard"},
        ],

        # CAT Verbal - Chapter 0: Reading Comprehension
        (exams[3], subjects[exams[3]][1], 0): [
            {"text": "Main purpose of reading is:", "options": [{"id": "a", "text": "Find all details"}, {"id": "b", "text": "Understand author's main idea"}, {"id": "c", "text": "Remember words"}, {"id": "d", "text": "Read fast"}], "correct": "b", "explanation": "Reading comprehension: understand author's main idea/theme", "difficulty": "easy"},
            {"text": "Inference in passage means:", "options": [{"id": "a", "text": "Stated directly"}, {"id": "b", "text": "Conclusion based on evidence"}, {"id": "c", "text": "Author's opinion"}, {"id": "d", "text": "Title of passage"}], "correct": "b", "explanation": "Inference: logical conclusion from given information", "difficulty": "medium"},
            {"text": "Tone of a passage can be:", "options": [{"id": "a", "text": "Happy, sad, angry"}, {"id": "b", "text": "Formal, informal"}, {"id": "c", "text": "Critical, supportive"}, {"id": "d", "text": "All of above"}], "correct": "d", "explanation": "Tone: author's attitude/emotion (formal, informal, critical, etc.)", "difficulty": "medium"},
            {"text": "To understand passage better, read:", "options": [{"id": "a", "text": "First sentence only"}, {"id": "b", "text": "All sentences carefully"}, {"id": "c", "text": "Quickly"}, {"id": "d", "text": "Only questions"}], "correct": "b", "explanation": "Read carefully to understand context and main idea", "difficulty": "easy"},
            {"text": "Passage context helps in understanding:", "options": [{"id": "a", "text": "Difficult words"}, {"id": "b", "text": "Author's intention"}, {"id": "c", "text": "Passage theme"}, {"id": "d", "text": "All of above"}], "correct": "d", "explanation": "Context: surrounding words/sentences help understand meaning", "difficulty": "hard"},
        ],
        # CAT Verbal - Chapter 1: Grammar
        (exams[3], subjects[exams[3]][1], 1): [
            {"text": "Subject-verb agreement means:", "options": [{"id": "a", "text": "Subject and verb same person/number"}, {"id": "b", "text": "Subject before verb"}, {"id": "c", "text": "Verb before subject"}, {"id": "d", "text": "No relation"}], "correct": "a", "explanation": "S-V agreement: 'He is' not 'He are'; 'They are' not 'They is'", "difficulty": "medium"},
            {"text": "Correct: 'Neither student ... their assignments':", "options": [{"id": "a", "text": "has completed"}, {"id": "b", "text": "have completed"}, {"id": "c", "text": "completes"}, {"id": "d", "text": "complete"}], "correct": "a", "explanation": "Neither (singular) takes singular verb 'has'", "difficulty": "hard"},
            {"text": "Pronoun must agree with:", "options": [{"id": "a", "text": "Verb only"}, {"id": "b", "text": "Noun (antecedent)"}, {"id": "c", "text": "Adjective"}, {"id": "d", "text": "Preposition"}], "correct": "b", "explanation": "Pronoun agrees with its noun antecedent in number/gender", "difficulty": "medium"},
            {"text": "'Each' is:", "options": [{"id": "a", "text": "Plural"}, {"id": "b", "text": "Singular"}, {"id": "c", "text": "Either"}, {"id": "d", "text": "Depends on context"}], "correct": "b", "explanation": "'Each' always singular: 'Each student is' not 'Each students are'", "difficulty": "medium"},
            {"text": "Verb tense for 'I __ here for 5 years':", "options": [{"id": "a", "text": "am"}, {"id": "b", "text": "have been"}, {"id": "c", "text": "was"}, {"id": "d", "text": "been"}], "correct": "b", "explanation": "Present perfect: 'have been' for duration from past to present", "difficulty": "hard"},
        ],
        # CAT Verbal - Chapter 2: Vocabulary
        (exams[3], subjects[exams[3]][1], 2): [
            {"text": "Synonym of 'abundant':", "options": [{"id": "a", "text": "Scarce"}, {"id": "b", "text": "Plentiful"}, {"id": "c", "text": "Rare"}, {"id": "d", "text": "Limited"}], "correct": "b", "explanation": "Abundant = plentiful, ample (opposite: scarce)", "difficulty": "medium"},
            {"text": "Antonym of 'verbose':", "options": [{"id": "a", "text": "Talkative"}, {"id": "b", "text": "Wordy"}, {"id": "c", "text": "Concise"}, {"id": "d", "text": "Loud"}], "correct": "c", "explanation": "Verbose = wordy, concise is opposite (brief, terse)", "difficulty": "medium"},
            {"text": "'Pragmatic' means:", "options": [{"id": "a", "text": "Idealistic"}, {"id": "b", "text": "Practical, realistic"}, {"id": "c", "text": "Theoretical"}, {"id": "d", "text": "Emotional"}], "correct": "b", "explanation": "Pragmatic: practical, realistic approach", "difficulty": "medium"},
            {"text": "'Ambiguous' means:", "options": [{"id": "a", "text": "Clear"}, {"id": "b", "text": "Having multiple meanings"}, {"id": "c", "text": "Obvious"}, {"id": "d", "text": "Specific"}], "correct": "b", "explanation": "Ambiguous: unclear, can have multiple interpretations", "difficulty": "medium"},
            {"text": "Use 'peruse' in context:", "options": [{"id": "a", "text": "To glance quickly"}, {"id": "b", "text": "To read carefully"}, {"id": "c", "text": "To skim"}, {"id": "d", "text": "To ignore"}], "correct": "b", "explanation": "Peruse: read carefully and thoroughly (not quickly)", "difficulty": "hard"},
        ],

        # CAT Data Interpretation - Chapter 0: Pie Charts
        (exams[3], subjects[exams[3]][2], 0): [
            {"text": "Pie chart shows:", "options": [{"id": "a", "text": "Change over time"}, {"id": "b", "text": "Parts of a whole"}, {"id": "c", "text": "Comparison between two"}, {"id": "d", "text": "Trends"}], "correct": "b", "explanation": "Pie chart: represents parts/percentages of a total", "difficulty": "easy"},
            {"text": "360° in pie chart represents:", "options": [{"id": "a", "text": "360 units"}, {"id": "b", "text": "100%"}, {"id": "c", "text": "360%"}, {"id": "d", "text": "100 units"}], "correct": "b", "explanation": "Full circle 360° = 100% of data", "difficulty": "easy"},
            {"text": "If sector has 90°, it represents:", "options": [{"id": "a", "text": "10%"}, {"id": "b", "text": "25%"}, {"id": "c", "text": "50%"}, {"id": "d", "text": "90%"}], "correct": "b", "explanation": "90°/360° × 100 = 25%", "difficulty": "medium"},
            {"text": "To compare values in pie chart:", "options": [{"id": "a", "text": "Look at angles"}, {"id": "b", "text": "Look at colors"}, {"id": "c", "text": "Look at labels"}, {"id": "d", "text": "a and c"}], "correct": "d", "explanation": "Compare angles (size of sector) and check labels/values", "difficulty": "medium"},
            {"text": "If you can't read exact value in pie chart:", "options": [{"id": "a", "text": "Guess"}, {"id": "b", "text": "Estimate from angle"}, {"id": "c", "text": "Ask for clarification"}, {"id": "d", "text": "Skip question"}], "correct": "b", "explanation": "Estimate from sector angle/size if value not clearly marked", "difficulty": "hard"},
        ],
        # CAT Data Interpretation - Chapter 1: Bar Graphs
        (exams[3], subjects[exams[3]][2], 1): [
            {"text": "Bar graph best for:", "options": [{"id": "a", "text": "Comparing values"}, {"id": "b", "text": "Showing parts of whole"}, {"id": "c", "text": "Trends over time"}, {"id": "d", "text": "Relationships"}], "correct": "a", "explanation": "Bar graphs: compare values across categories easily", "difficulty": "easy"},
            {"text": "If bar height = 5 cm and scale = 10 units/cm:", "options": [{"id": "a", "text": "50 units"}, {"id": "b", "text": "5 units"}, {"id": "c", "text": "500 units"}, {"id": "d", "text": "2 units"}], "correct": "a", "explanation": "Value = height × scale = 5 × 10 = 50 units", "difficulty": "medium"},
            {"text": "Horizontal bar graph is used for:", "options": [{"id": "a", "text": "Long category names"}, {"id": "b", "text": "Many categories"}, {"id": "c", "text": "Both"}, {"id": "d", "text": "Time series"}], "correct": "c", "explanation": "Horizontal bars better for long names or many categories", "difficulty": "medium"},
            {"text": "To find highest value in bar graph:", "options": [{"id": "a", "text": "Look at tallest bar"}, {"id": "b", "text": "Read all values"}, {"id": "c", "text": "Check scale"}, {"id": "d", "text": "Estimate visually"}], "correct": "a", "explanation": "Tallest bar represents highest value", "difficulty": "easy"},
            {"text": "Grouped bar graph compares:", "options": [{"id": "a", "text": "Single category"}, {"id": "b", "text": "Two or more categories"}, {"id": "c", "text": "Time periods"}, {"id": "d", "text": "Percentages"}], "correct": "b", "explanation": "Grouped bars: compare multiple categories side-by-side", "difficulty": "medium"},
        ],
        # CAT Data Interpretation - Chapter 2: Tables
        (exams[3], subjects[exams[3]][2], 2): [
            {"text": "Table is organized by:", "options": [{"id": "a", "text": "Rows only"}, {"id": "b", "text": "Columns only"}, {"id": "c", "text": "Rows and columns"}, {"id": "d", "text": "None"}], "correct": "c", "explanation": "Table: data organized in rows (horizontal) and columns (vertical)", "difficulty": "easy"},
            {"text": "To find intersection in table:", "options": [{"id": "a", "text": "Find row and column"}, {"id": "b", "text": "Look down/across"}, {"id": "c", "text": "Follow row to column"}, {"id": "d", "text": "All of above"}], "correct": "d", "explanation": "Find row and column, trace where they meet for value", "difficulty": "easy"},
            {"text": "If table has missing value, you can:", "options": [{"id": "a", "text": "Leave blank"}, {"id": "b", "text": "Calculate from other data"}, {"id": "c", "text": "Skip question"}, {"id": "d", "text": "Guess"}], "correct": "b", "explanation": "Use relationships/totals to calculate missing values", "difficulty": "hard"},
            {"text": "Total in row/column found by:", "options": [{"id": "a", "text": "Adding all values"}, {"id": "b", "text": "Subtracting"}, {"id": "c", "text": "Multiplying"}, {"id": "d", "text": "Dividing"}], "correct": "a", "explanation": "Total = sum of all values in row/column", "difficulty": "easy"},
            {"text": "Table header shows:", "options": [{"id": "a", "text": "Column names"}, {"id": "b", "text": "Row names"}, {"id": "c", "text": "Both"}, {"id": "d", "text": "Totals"}], "correct": "c", "explanation": "Headers: column titles at top, row labels on left", "difficulty": "medium"},
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
        "message": "Database seeded successfully with all chapters and questions!",
        "users": len(users),
        "exams": len(exam_data),
        "subjects": sum(len(v) for v in subjects.values()),
        "chapters": sum(len(v) for v in chapters.values()),
        "questions": sum(len(v) for v in q_ids_by_chapter.values()),
        "users_list": [{"id": uid, "name": n} for uid, (n, e, a) in zip(users, user_names)]
    }

@router.get("/users")
async def get_users():
    users = await users_col.find({}, {"_id": 1, "name": 1, "email": 1, "avatar": 1}).to_list(None)
    return serialize_list(users)
