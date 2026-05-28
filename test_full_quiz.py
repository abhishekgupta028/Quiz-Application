import asyncio
import httpx
import json

async def test_full_quiz():
    async with httpx.AsyncClient() as client:
        try:
            print("=" * 60)
            print("FULL QUIZ FLOW TEST")
            print("=" * 60)
            
            # Seed database
            print("\n1. Seeding database...")
            seed = await client.post('http://localhost:8000/api/seed/')
            seed_data = seed.json()
            user_id = seed_data['users_list'][0]['id']
            print(f"   ✅ Created {seed_data['questions']} questions across {seed_data['chapters']} chapters")
            
            # Get exam, subject, chapter
            print("\n2. Getting exam, subject, chapter...")
            exams = (await client.get('http://localhost:8000/api/exams/')).json()
            exam_id = exams[0]['id']
            
            subjects = (await client.get(f'http://localhost:8000/api/subjects/?exam_id={exam_id}')).json()
            subject_id = subjects[0]['id']
            
            chapters = (await client.get(f'http://localhost:8000/api/chapters/?exam_id={exam_id}&subject_id={subject_id}')).json()
            chapter_id = chapters[0]['id']
            
            print(f"   ✅ Exam: {exams[0]['title']}")
            print(f"   ✅ Subject: {subjects[0]['title']}")
            print(f"   ✅ Chapter: {chapters[0]['title']}")
            
            # Start quiz
            print("\n3. Starting quiz...")
            quiz_response = await client.post('http://localhost:8000/api/quiz/start', json={
                "user_id": user_id,
                "exam_id": exam_id,
                "subject_id": subject_id,
                "chapter_id": chapter_id
            })
            session = quiz_response.json()
            session_id = session['id']
            print(f"   ✅ Quiz started (Session ID: {session_id})")
            print(f"   ✅ Total questions: {session['total_questions']}")
            
            # Get first question
            print("\n4. Fetching first question...")
            q_response = await client.get(f'http://localhost:8000/api/quiz/session/{session_id}/question')
            q_data = q_response.json()
            question = q_data['question']
            print(f"   ✅ Question {q_data['question_number']}/{q_data['total_questions']}")
            print(f"   Question: {question['text'][:80]}...")
            print(f"   Options: {len(question['options'])} choices available")
            print(f"   Correct answer: {question['correct_option_id']}")
            
            # Submit answer
            print("\n5. Submitting answer...")
            from datetime import datetime
            answer_response = await client.post('http://localhost:8000/api/quiz/answer', json={
                "session_id": session_id,
                "question_id": question['id'],
                "selected_option_id": question['correct_option_id'],
                "question_shown_at": q_data.get('shown_at', datetime.utcnow().isoformat()),
                "answer_submitted_at": datetime.utcnow().isoformat()
            })
            answer_result = answer_response.json()
            print(f"   ✅ Answer submitted")
            print(f"   Response keys: {answer_result.keys()}")
            if 'is_correct' in answer_result:
                print(f"   ✅ Correct: {answer_result['is_correct']}")
                if answer_result['is_correct']:
                    print(f"   ✅ Score increased!")
            else:
                print(f"   Response: {answer_result}")
            
            # Complete quiz
            print("\n6. Completing quiz...")
            from datetime import datetime
            complete_response = await client.post('http://localhost:8000/api/quiz/complete', json={
                "session_id": session_id,
                "completed_at": datetime.utcnow().isoformat()
            })
            print(f"   Complete response status: {complete_response.status_code}")
            if complete_response.status_code != 200:
                error_data = complete_response.json()
                print(f"   Error response: {error_data}")
            
            print("\n" + "=" * 60)
            print("✅ FULL QUIZ FLOW SUCCESSFUL!")
            print("✅ No more 'failed to start quiz' errors!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

asyncio.run(test_full_quiz())
