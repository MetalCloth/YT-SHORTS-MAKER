import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import dotenv
from dotenv import load_dotenv
load_dotenv()

from unrealspeech import UnrealSpeechAPI

load_dotenv() 
app=FastAPI()

api_key = os.getenv("UNREAL_SPEECH_API_KEY") 


speech_api=UnrealSpeechAPI(api_key)

voices=[]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/voice')
async def post_voice(request:Request):
    data=await request.json()
    data=data.get('message')

    voices.append(data)
    return {'data':voices}



@app.get('/api/voice')
async def get_voice():
    latest_voice= voices[len(voices)-1] if len(voices)>0 else ''

    if latest_voice!='':
        try:
            audio_data =  speech_api.speech(
            text=latest_voice,
            voice_id="Will"
        )
            return {'url':audio_data['OutputUri']}

        except Exception as e:
            print(f"Alert MA KA BHOOSADA AAAAAG")
            print(e)
    


    return {'voice':latest_voice,'all_voices':voices}





# if not api_key:
#     raise ValueError("API key not found! Check your .env file and variable name.")
# # ---------------------

# speech_api = UnrealSpeechAPI(api_key=api_key)
# print("✅ API Client Initialized Successfully!")

# # 4. Use one of its methods within a try...except block.
# try:
#     print("Generating audio...")
#     audio_data = speech_api.speech(
#         text="This is a test of the API wrapper.",
#         voice_id="Will"
#     )
    
#     print("Playing audio...")
#     print(audio_data)
#     print("Done.")

# except Exception as e:
#     print(f"An error occurred during API call: {e}")