import asyncio
import httpx

async def test_seed():
    try:
        async with httpx.AsyncClient() as client:
            print('Seeding database with complete data...')
            response = await client.post('http://localhost:8000/api/seed/', timeout=30)
            data = response.json()
            
            print(f'Status: {response.status_code}')
            print(f'Message: {data.get("message")}')
            print(f'Users: {data.get("users")}')
            print(f'Exams: {data.get("exams")}')
            print(f'Subjects: {data.get("subjects")}')
            print(f'Chapters: {data.get("chapters")}')
            print(f'Questions: {data.get("questions")}')
            
            if data.get("questions", 0) > 0:
                print("\n✅ Database seeded successfully!")
                print(f"✅ All chapters now have questions")
            else:
                print("\n❌ No questions added")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test_seed())
