import asyncio
import httpx

async def verify_questions():
    async with httpx.AsyncClient() as client:
        try:
            # Seed database
            print("Seeding database...")
            seed = await client.post('http://localhost:8000/api/seed/')
            seed_data = seed.json()
            user_id = seed_data['users_list'][0]['id']
            print(f"Users seeded: {seed_data['users']}")
            print(f"Questions created: {seed_data['questions']}\n")
            
            # Get exams
            exams = await client.get('http://localhost:8000/api/exams/')
            exam_id = exams.json()[0]['id']
            
            # Get subjects
            subjects = await client.get(f'http://localhost:8000/api/subjects/?exam_id={exam_id}')
            subject_id = subjects.json()[0]['id']
            
            # Get chapters
            chapters = await client.get(f'http://localhost:8000/api/chapters/?exam_id={exam_id}&subject_id={subject_id}')
            chapter_id = chapters.json()[0]['id']
            
            # Check questions in database directly
            questions = await client.get(f'http://localhost:8000/api/questions/?chapter_id={chapter_id}')
            questions_data = questions.json()
            
            print(f"Questions for first chapter: {len(questions_data)}")
            if questions_data:
                q = questions_data[0]
                print(f"Sample question: {q.get('text', 'N/A')[:80]}...")
                print(f"Options: {len(q.get('options', []))} options")
            
            # Now test quiz start
            quiz_data = {
                "user_id": user_id,
                "exam_id": exam_id,
                "subject_id": subject_id,
                "chapter_id": chapter_id
            }
            
            print(f"\nStarting quiz...")
            response = await client.post('http://localhost:8000/api/quiz/start', json=quiz_data)
            quiz = response.json()
            print(f"Quiz response keys: {quiz.keys()}")
            print(f"Questions in quiz: {len(quiz.get('questions', []))}")
            
            if quiz.get('questions'):
                print(f"First quiz question: {quiz['questions'][0]}")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

asyncio.run(verify_questions())
