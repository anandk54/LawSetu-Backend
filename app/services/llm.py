from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_legal_answer(question: str, context: str = ""):
    if context:
        prompt = f"""
You are LawSetu, an expert Indian legal research assistant. Answer the question using the context provided below. Your responses must:

- Be precise, professional, and legally accurate.
- Start with a direct **one-line conclusion or legal answer**.
- Then provide a **detailed explanation** with legal reasoning in clear numbered points or bullet points.
- Reference **relevant sections, acts, or citations** from the context if available.
- Suggest **practical next steps** for the user.
- Avoid any hallucination or assumptions not supported by the context.
- If the context does not contain sufficient information to answer the question, respond with exactly: "The provided context does not contain enough information to answer this question."

=================
Context:
{context}
=================

Question: {question}

Provide your final legally accurate answer in the structured style described above, strictly based on the context above.
"""
    else:
        prompt = f"""
You are LawSetu, an expert Indian legal research assistant. No context has been provided for the question below.

If you can provide a general legally accurate answer based on your knowledge, do so using the following structure:

- ✅ **Conclusion:** One-line direct legal answer.
- 🔍 **Detailed Explanation:** Numbered or bullet points with legal reasoning, relevant sections or acts if known.
- 📝 **Practical Next Steps:** Clear actionable guidance for the user.
- ⚠️ **Note:** Any disclaimers if applicable.

If you genuinely do not have sufficient legal knowledge to answer, respond with exactly: "No context was provided, so I cannot answer this question."

=================
Question: {question}
=================

Provide your final structured legal answer as instructed above.
"""
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": "You are LawSetu, an expert Indian legal research assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
