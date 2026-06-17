from groq import AsyncGroq
from dotenv import load_dotenv
import os 

load_dotenv()


client = AsyncGroq(api_key=os.getenv("groq_token"))

async def ask_ai( user_message: str ):

    response = await client.chat.completions.create(
          model="Llama-3.3-70b-versatile",
          messages=[
               {"role": "user", "content": user_message }
          ]
     )

    return response.choices[0].message.content