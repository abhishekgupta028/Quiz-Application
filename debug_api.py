import asyncio
import httpx

async def debug_response():
    async with httpx.AsyncClient() as client:
        try:
            # Get exams
            exams_response = await client.get('http://localhost:8000/api/exams/')
            print(f"Status: {exams_response.status_code}")
            print(f"Response type: {type(exams_response.json())}")
            data = exams_response.json()
            print(f"Response: {data}")
            
            if isinstance(data, list) and len(data) > 0:
                print(f"First exam: {data[0]}")
                
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

asyncio.run(debug_response())
