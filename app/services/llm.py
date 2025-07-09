from dotenv import load_dotenv
import os
from openai import OpenAI
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_legal_answer(question: str):
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": "You are a legal assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content
