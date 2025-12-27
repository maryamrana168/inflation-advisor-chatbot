import gradio as gr
import os
import requests

# Load GROQ API Key from environment variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-8b-8192"

# ===============================
# 🔹 SYSTEM PROMPT (INFLATION BOT)
# ===============================
SYSTEM_PROMPT = """
You are Inflation Survival Advisor Bot 📉📊, a smart financial assistant.
Your job is to help users survive inflation by managing expenses wisely.

You:
- Explain how inflation affects daily spending
- Suggest cheaper alternatives and budget-friendly brands
- Help users adjust monthly budgets dynamically
- Give practical money-saving tips
- Keep advice simple, realistic, and actionable

You do NOT give investment or stock trading advice.
"""

def query_groq(message, chat_history):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for user, bot in chat_history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})

    messages.append({"role": "user", "content": message})

    response = requests.post(
        GROQ_API_URL,
        headers=headers,
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.6
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"

def respond(message, chat_history):
    bot_reply = query_groq(message, chat_history)
    chat_history.append((message, bot_reply))
    return "", chat_history

# ===============================
# 🔹 GRADIO UI
# ===============================
with gr.Blocks() as demo:
    gr.Markdown("## 📉 Inflation Survival Advisor Bot")
    gr.Markdown("Smart budgeting and spending advice during inflation")

    chatbot = gr.Chatbot(height=420)
    msg = gr.Textbox(
        label="Ask about budgeting, prices, or saving money",
        placeholder="e.g. My grocery bill increased, what should I do?"
    )
    clear = gr.Button("Clear Chat")
    state = gr.State([])

    msg.submit(respond, [msg, state], [msg, chatbot])
    clear.click(lambda: ([], []), None, [chatbot, state])

demo.launch()
