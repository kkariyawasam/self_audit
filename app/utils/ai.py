import openai
import os
import re
import json

openai.api_key = os.getenv("OPENAI_API_KEY")


def evaluate_control_final(question_id: int, clarification_text: str, evidence_files: list):
    """
    Use GPT-4 to evaluate compliance based on clarification and evidence.
    """

    evidence_summary = ', '.join(evidence_files)

    prompt = f"""
You are a compliance auditor assistant helping evaluate whether a control is satisfied for a certification like ISO 27001.

Here’s the input:
- Control Question ID: {question_id}
- Clarification from client: "{clarification_text}"
- Evidence provided: {evidence_summary}

Based on this, assess whether the control is compliant or not. Give a yes/no answer and explain your reasoning.
Respond in JSON format like this:
{{
  "is_compliant": true/false,
  "reasoning": "your explanation here"
}}
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
        
        response_content  = response.choices[0].message.content
        match = re.search(r'```json\s*(\{.*?\})\s*```', response_content, re.DOTALL)
        
        if match:
            inner_json = json.loads(match.group(1))
            reasoning_text = inner_json.get('reasoning')
            print(reasoning_text)
        else:
            print("Could not extract inner JSON.")
            
        return {
           "is_compliant": True,
            "reasoning": reasoning_text
        }

    except Exception as e:
        return {
            "is_compliant": False,
            "reasoning": f"Error during evaluation: {str(e)}"
        }