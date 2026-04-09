

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a presentation designer.
Return ONLY a valid JSON object. No explanation. No markdown. No code fences.

Use this exact structure:
{
  "title": "Main presentation title",
  "subtitle": "Short tagline",
  "slides": [
    {
      "heading": "Slide title",
      "bullets": ["Point one", "Point two", "Point three"],
      "speaker_note": "What to say here"
    }
  ]
}

Rules:
- Exactly 6 slides
- 3-4 bullets per slide, each under 12 words
- First slide: Introduction
- Last slide: Conclusion
- Return ONLY JSON. Nothing else.
"""

def generate_slide_content(topic: str) -> dict:
    print(f"Asking Groq about: '{topic}'...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Topic: {topic}"}
        ]
    )

    raw = response.choices[0].message.content

    # Clean response
    cleaned = re.sub(r"```json|```", "", raw).strip()

    try:
        data = json.loads(cleaned)
    except Exception as e:
        print("❌ JSON parsing failed")
        print("Raw response:", raw)
        return None

    print(f"✅ Got {len(data['slides'])} slides!")
    return data