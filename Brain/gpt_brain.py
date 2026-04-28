import os
import json
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        client = None
        print("[GPT] No OPENAI_API_KEY set. GPT cloud fallback disabled (using Ollama only).")
except ImportError:
    client = None
    print("[GPT] openai module not found. AI capabilities will be limited.")
except Exception as e:
    client = None
    print(f"[GPT] Failed to initialize OpenAI client: {e}")

def ask_gpt(user_input):
    if not client:
        # Fallback to general chat if OpenAI is not available
        return {
            "intent": "general_chat",
            "response": "OpenAI module is missing. I cannot process complex requests.",
            "parameters": {}
        }
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Jarvis, an AI assistant.

You MUST respond strictly in JSON format.

Available intents:
1. general_chat
2. weather
3. send_whatsapp
4. open_app
5. time_query

Respond like this:
{
  "intent": "intent_name",
  "response": "what you want to say to user",
  "parameters": {}
}
"""
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content
        return json.loads(reply)

    except Exception as e:
        return {
            "intent": "general_chat",
            "response": "Sorry, I encountered an error.",
            "parameters": {}
        }