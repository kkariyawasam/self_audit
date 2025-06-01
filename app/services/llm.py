import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_ai_with_context(question: str, document_context: str) -> str:
    prompt = f"""
You are an audit assistant helping with ISO 27001 readiness checks.

Based on the following documentation, evaluate the client's readiness for the control:

CONTROL QUESTION:
{question}

DOCUMENTATION:
{document_context}

Evaluate whether the documentation provides sufficient evidence or if clarification or real-world evidence is needed.
Give your reasoning clearly.

Answer:
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
             messages=[
            {"role": "user", "content": prompt}
          ],
            temperature=0.2,
            max_tokens=500
        )
        

        return (response.choices[0].message.content)
    except Exception as e:
        return f"Error from AI: {str(e)}"