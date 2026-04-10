

# import os
# import json
# import re
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# SYSTEM_PROMPT = """You are a presentation designer.
# Return ONLY a valid JSON object.

# Structure:
# {
#   "title": "Main title",
#   "subtitle": "Short tagline",
#   "slides": [
#     {
#       "heading": "Slide title",
#       "bullets": ["Point 1", "Point 2"],
#       "speaker_note": "Explain here"
#     }
#   ]
# }
# """

# def generate_slide_content(topic: str, extra: str = "", num_slides: int = 6) -> dict:
#     print(f"Asking AI about: {topic}")

#     prompt = f"Topic: {topic}\nCreate exactly {num_slides} slides."

#     if extra:
#         prompt += f"\nExtra instructions: {extra}"

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": prompt}
#         ]
#     )

#     raw = response.choices[0].message.content
#     cleaned = re.sub(r"```json|```", "", raw).strip()

#     try:
#         data = json.loads(cleaned)
#         return data
#     except:
#         print("Error parsing JSON")
#         print(raw)
#         return None 
import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🔥 UPGRADED PROMPT (INSANE QUALITY)
SYSTEM_PROMPT = """
You are a world-class presentation designer.

Create highly engaging, professional, and visually appealing slides.

Rules:
- Use powerful, concise bullet points
- Make content clear, structured, and impactful
- Add storytelling flow across slides
- Use modern business language
- Each slide should feel purposeful and well-designed

Strict Instructions:
- Return ONLY valid JSON (no explanation, no markdown, no extra text)
- Follow this exact structure:

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
"""

def generate_slide_content(topic: str, extra: str = "", num_slides: int = 6) -> dict:
    print(f"Asking AI about: {topic}")

    prompt = f"Topic: {topic}\nCreate exactly {num_slides} slides."

    if extra:
        prompt += f"\nExtra instructions: {extra}"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )

        raw = response.choices[0].message.content

        # Clean unwanted markdown if any
        cleaned = re.sub(r"```json|```", "", raw).strip()

        data = json.loads(cleaned)

        print(f"✅ Generated {len(data['slides'])} slides")

        return data

    except Exception as e:
        print("❌ ERROR generating slides:", e)
        print("Raw response:", raw if 'raw' in locals() else "No response")
        return None
