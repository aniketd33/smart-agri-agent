from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert agricultural assistant for Indian farmers.
You have deep knowledge about:
- Indian crops (Kharif, Rabi, Zaid seasons)
- Soil types and management (Black, Loamy, Red soil)
- Pest and disease management
- Irrigation techniques
- Fertilizer recommendations (NPK)
- Government schemes for farmers (PM-KISAN, Fasal Bima)
- Market prices and selling strategies
- Organic farming practices
- Weather impact on crops

Always give practical, actionable advice suitable for Indian farming conditions.
Keep responses concise and easy to understand.
Use simple language — farmers may not be highly technical."""

def get_chat_response(messages):
    try:
        groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in messages:
            groq_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=groq_messages,
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message.content, None

    except Exception as e:
        return None, str(e)