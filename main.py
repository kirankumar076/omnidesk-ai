from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

from rag_store import retrival
from guardrails import input_guard,check_order_status,issue_refund

load_dotenv()
app=FastAPI(title="OmniDesk AI Support Engine")
client=genai.Client()

class SupportTicket(BaseModel):
    message:str
@app.post("/support")

def handle_support(ticket: SupportTicket):
    safety=input_guard(ticket.message)
    if safety.is_safe == False:
        return {"status": "blocked", "reply": f"Blocked by Guardrail: {safety.reason}"}

    chat= client.chats.create(
        model="gemini-3.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are the OmniDesk AI Support Agent. Use your tools to check company policies, check order status, and issue refunds when appropriate.",
            tools=[retrival,check_order_status,issue_refund],
            temperature=0.0
        )
    )
    response = chat.send_message(ticket.message)
    return {"status":"success","reply":response.text}