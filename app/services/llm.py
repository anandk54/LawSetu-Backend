from openai import OpenAI

client = OpenAI()

def get_legal_answer(question: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a legal assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content
