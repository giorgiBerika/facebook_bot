from fastapi import FastAPI, Query, HTTPException, status, Request
from starlette.responses import PlainTextResponse
from dotenv import load_dotenv
import os 
import httpx

from ai_bot import ask_ai 

load_dotenv()

app = FastAPI() 


# Webhook verification endpoint 
@app.get("/webhook")
def verify_webhook( mode: str = Query(alias="hub.mode"),
                    token: str = Query(alias="hub.verify_token"),
                    challenge: str = Query(alias="hub.challenge")   ):
    
    real_token = os.getenv("my_token")

    if (mode != "subscribe" or token != real_token ):   
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token does not match!"
        )

    return PlainTextResponse(challenge)

# Helper function to send messages back to users
async def send_message(sender_id: int, message_txt: str):
    access_token = os.getenv("access_token")
    url = 'https://graph.facebook.com/v22.0/me/messages'
   
    payload = {
        "recipient": {"id": sender_id},
        "message" : {"text": message_txt}
    }
    params = {"access_token": access_token }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, params=params )
        return response.json()

@app.post("/webhook")
async def get_message( request: Request ): 
    user_info = await request.json()

    entries = user_info.get("entry")
    for entry in entries:
        for msg in entry.get("messaging"):
            sender = msg.get("sender").get("id")
            content = msg.get("message").get("text")

            ai_response = await ask_ai(content)
            await send_message(sender_id=sender, message_txt=ai_response)
    return {"status": "ok"}




