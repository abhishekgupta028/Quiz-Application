import asyncio
import httpx

async def test_quiz_start():
    async with httpx.AsyncClient() as client:
        try:
            # Seed the database and get user_id from response
            print("Seeding database...")
            seed_response = await client.post('http://localhost:8000/api/seed/')
            seed_data = seed_response.json()
            
            if not seed_data.get('users_list'):
                print("❌ No users found in seed response")
                return
            
            user_id = seed_data['users_list'][0]['id']
            print(f"Using user: {user_id}\n")
            
            # Get exams
            exams_response = await client.get('http://localhost:8000/api/exams/')
            exams = exams_response.json()
            
            if not exams:
                print("❌ No exams found")
                return
            
            exam_id = exams[0]['id']
            print(f"Testing with Exam: {exams[0]['title']}")
            
            # Get subjects for this exam
            subjects_response = await client.get(f'http://localhost:8000/api/subjects/?exam_id={exam_id}')
            subjects = subjects_response.json()
            
            if not subjects:
                print("❌ No subjects found")
                return
                
            subject_id = subjects[0]['id']
            print(f"Testing with Subject: {subjects[0]['title']}")
            
            # Get chapters for this subject
            chapters_response = await client.get(f'http://localhost:8000/api/chapters/?exam_id={exam_id}&subject_id={subject_id}')
            chapters = chapters_response.json()
            
            if not chapters:
                print("❌ No chapters found")
                return
            
            print(f"\nTesting quiz start for {len(chapters)} chapters:")
            print("=" * 60)
            
            success_count = 0
            failed_chapters = []
            
            for i, chapter in enumerate(chapters, 1):
                chapter_id = chapter['id']
                chapter_name = chapter['title']
                
                # Try to start a quiz
                quiz_data = {
                    "user_id": user_id,
                    "exam_id": exam_id,
                    "subject_id": subject_id,
                    "chapter_id": chapter_id
                }
                
                response = await client.post('http://localhost:8000/api/quiz/start', json=quiz_data)
                
                if response.status_code == 200:
                    quiz = response.json()
                    questions_count = len(quiz.get('questions', []))
                    print(f"✅ Chapter {i}: {chapter_name} - {questions_count} questions loaded")
                    success_count += 1
                else:
                    error = response.json()
                    print(f"❌ Chapter {i}: {chapter_name} - Error: {error.get('detail', 'Unknown error')}")
                    failed_chapters.append(chapter_name)
            
            print("=" * 60)
            print(f"\n✅ Quiz Start Results: {success_count}/{len(chapters)} chapters successful")
            
            if failed_chapters:
                print(f"❌ Failed chapters: {', '.join(failed_chapters)}")
            else:
                print("✅ All chapters can now start quizzes without errors!")
                
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

asyncio.run(test_quiz_start())
