import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set")

client = Groq(api_key=GROQ_API_KEY)


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set")

client = Groq(api_key=GROQ_API_KEY)

def analyze_medical_report(report_text: str) -> str:
    """Full structured AI analysis of a medical report."""
    prompt = f"""You are an expert AI medical assistant. Analyze the following medical report carefully and provide a comprehensive, patient-friendly response.

Structure your response with these sections using markdown:

## 1. 🩺 Possible Illness / Diagnosis
## 2. ⚠️ Risk Level
(Low / Moderate / High / Critical — with brief explanation)

## 3. 📋 Important Findings
(List each abnormal value and what it means in simple language)

## 4. 💊 Suggested Treatments
(General treatment approaches — always recommend consulting a doctor)

## 5. 🥗 Diet Recommendations
(Specific dietary advice based on findings)

## 6. 👨‍⚕️ Recommended Specialist
(Type of doctor to see, and why)

## 7. 🚨 Emergency Level
(Immediate / Within 48 hours / Within 2 weeks / Routine follow-up)

## 8. 📝 Additional Notes
(Any other important observations)

Medical Report:
{report_text}

Important: Always remind the patient that AI analysis is not a substitute for professional medical advice.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.3,
    )
    return response.choices[0].message.content


def chat_with_ai(messages: list, report_context: str = "") -> str:
    """Multi-turn health chatbot using Groq."""
    system_prompt = f"""You are MediScan AI, a friendly and knowledgeable medical assistant chatbot.
You help patients understand their medical reports, explain medical terms in simple language,
provide general health advice, and recommend appropriate specialists.

Always:
- Use simple, clear language
- Be empathetic and supportive
- Remind users to consult a real doctor for diagnosis/treatment
- Keep responses concise but thorough
- Use bullet points and emojis to make responses easy to read

Patient's latest medical report context:
{report_context if report_context else "No report uploaded yet."}

Do NOT provide definitive diagnoses. Always recommend professional medical consultation.
"""
    groq_messages = [{"role": "system", "content": system_prompt}]
    for msg in messages[-10:]:  # last 10 messages for context window
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=groq_messages,
        max_tokens=800,
        temperature=0.5,
    )
    return response.choices[0].message.content