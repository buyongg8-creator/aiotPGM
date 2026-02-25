from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='부산역에 위치한 대한상공회의소 부산인력개발원에 대해 알려줘'
)

print(response.text)