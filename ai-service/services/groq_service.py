import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_response(prompt, contract_text):

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": contract_text
                }
            ],
            temperature=0.3,
            max_tokens=800
        )

        content = response.choices[0].message.content

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        try:
            return json.loads(content)

        except Exception:
            return {
                "raw_response": content
            }

    except Exception as e:

        return {
            "error": str(e),
            "is_fallback": True
        }