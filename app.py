from datetime import datetime
from fastapi import FastAPI, Form, Request
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.voice_response import VoiceResponse
from fastapi.responses import Response
from openai import OpenAI

from dotenv import dotenv_values

env = dotenv_values('.env')


CHAT_PROMPT = "You are a helpful assistant that can answer questions and help with tasks. You are also a great listener and can provide emotional support."

chat_history = [
    {"role": "system", "content": CHAT_PROMPT + f"The user lives in San Fransisco, CA. The time zone is PST. The current time is: {datetime.now().strftime('%H:%M:%S')}"},
]

openai_client = OpenAI(
        api_key=env['OPENAI_API_KEY'],

)

app = FastAPI(
    title="My API",
    description="A basic FastAPI application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the API"}


@app.post("/answer")
async def answer( response_bool: Optional[bool] = None):
    try:
        resp = VoiceResponse()
        
        # Gather speech input from the caller
        gather = resp.gather(
            input='speech',
            action='/process-speech',
            language='en-US',
            speechTimeout='auto',
            enhanced=True,
            hints=['hello', 'hi', 'test'],  # Add common words to improve recognition
            profanityFilter=False,          # Disable profanity filter for better accuracy
            timeout=3                       # Wait 3 seconds for speech to begin
        )
        
        # Make the prompt clearer
        if not response_bool:
            gather.say("Please speak now. I'm listening.", voice='Polly.Amy')
        else:
            gather.say(" ", voice='Polly.Amy')
        # If user doesn't say anything, try again
        resp.redirect('/answer')
        
        return Response(
            content=str(resp),
            media_type="application/xml"
        )
    except Exception as e:
        print(f"Error in answer: {str(e)}")
        return {"error": str(e)}

@app.post("/process-speech")
async def process_speech(request: Request):
    try:
        # Get form data from the request
        form_data = await request.form()
        speech_result = form_data.get('SpeechResult')
        
        resp = VoiceResponse()
        
        if speech_result:
            print(f"Transcribed text: {speech_result}")
            chat_history.append({"role": "user", "content": speech_result})
            agent_message = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=chat_history
            )

            print(f"Agent Message: {agent_message.choices[0].message.content}")
            chat_history.append({"role": "assistant", "content": agent_message.choices[0].message.content})
            resp.say(agent_message.choices[0].message.content, voice='Polly.Amy')
            resp.redirect('/answer?response_bool=True')
        else:
            print("No speech detected")
            resp.say("I didn't catch that. Please try again.", voice='Polly.Amy')
            resp.redirect('/answer')
        
        return Response(
            content=str(resp),
            media_type="application/xml"
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
