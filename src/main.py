import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import ffmpeg
import dotenv
import json
import requests
from dotenv import load_dotenv
load_dotenv()

from unrealspeech import UnrealSpeechAPI

load_dotenv() 
app=FastAPI()

api_key = os.getenv("UNREAL_SPEECH_API_KEY") 


speech_api=UnrealSpeechAPI(api_key)

voices=[]

video=[]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/voice')
async def post_voice(request:Request):
    response=await request.json()
    data=response.get('message')

    mp4=response.get('video')

    voices.append(data)

    video.append(mp4)
    return {'data':voices,'video':video}



@app.get('/api/voice')
async def get_voice():
    latest_voice= voices[len(voices)-1] if len(voices)>0 else ''

    if latest_voice!='':
        try: 
            audio_data = speech_api.speech(
            text=latest_voice,
            voice_id="Will",      # Choose voice: Scarlett, Dan, Liv, etc.
            timestamp_type="word",    # word or sentence
            bitrate="192k",
            pitch=0.92
        )
            return preprocess(audio_data=audio_data)

        except Exception as e:
            print(f"Alert MA KA BHOOSADA AAAAAG")
            print(e)
    

    return {'voice':latest_voice,'all_voices':voices}



def preprocess(audio_data):
    audio=requests.get(audio_data['OutputUri'])


    mp4=video[len(video)-1]

    with open('test.mp3','wb') as file:
        file.write(audio.content)

    timestamp=requests.get(audio_data['TimestampsUri'])

    data_str = (timestamp.content).decode("utf-8")  # bytes → string
    data_json = json.loads(data_str) 

    phrases=group_words_into_phrases(data_json)

    function(input_file=mp4,audio_file="test.mp3",output_file='output.mp4',data_json=data_json,phrases=phrases)


    return {'output':'Fucking completed work'}



def group_words_into_phrases(words, max_words_per_phrase=3):
    """Groups individual words (dict format) into phrases based on punctuation or max word count."""
    phrases = []
    current_phrase = []
    if not words:
        return []

    phrase_start_time = words[0]["start"]

    for i, w in enumerate(words):
        word = w["word"]
        start = w["start"]
        end = w["end"]

        current_phrase.append(word)
        should_end_phrase = (
            any(c in word for c in ",.?!")
            or len(current_phrase) >= max_words_per_phrase
            or i == len(words) - 1
        )

        if should_end_phrase:
            phrase_text = " ".join(current_phrase)
            phrases.append({
                "phrase": phrase_text,
                "start": phrase_start_time,
                "end": end
            })
            current_phrase = []
            if i < len(words) - 1:
                phrase_start_time = words[i + 1]["start"]

    return phrases



def add_timed_text(stream, text, start, end, max_font_ratio=0.08, min_font_ratio=0.05,
                   fontcolor="white", outline=6):
    """
    Adds centered text that auto-shrinks for long words.
    """
    font_ratio = max(min_font_ratio, max_font_ratio - (len(text) / 50) * 0.01)

    return stream.drawtext(
        text=text,
        fontfile=r"C:\Windows\Fonts\impact.ttf",
        fontsize=f"w*{font_ratio}",
        fontcolor=fontcolor,
        x="(w-text_w)/2",
        y="(h-text_h)/2",
        borderw=outline,
        bordercolor="black",
        box=0,
        enable=f"between(t,{start},{end})"
    )


def overlay(stream, phrases):
    """
    Apply timed phrases to the video stream.
    phrases: list of dicts with keys 'phrase', 'start', 'end'
    """
    for p in phrases:
        stream = add_timed_text(stream, p["phrase"], p["start"], p["end"])
    return stream



def function(input_file,audio_file,output_file,data_json,phrases):
    audio_duration=data_json[len(data_json)-1]['end']+0.5

    video=ffmpeg.input(input_file,stream_loop=-1,t=audio_duration).video
    audio=ffmpeg.input(audio_file).audio

    video=overlay(video,phrases)

    (
    ffmpeg
    .output(video, audio, output_file, vcodec='libx264', acodec='aac', strict='experimental')
    .overwrite_output()
    .run()
)
    









# if not api_key: