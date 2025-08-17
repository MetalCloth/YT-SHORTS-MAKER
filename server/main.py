import os
import json
import requests
import azure.cognitiveservices.speech as speechsdk
import ffmpeg
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from unrealspeech import UnrealSpeechAPI

# --- Initialization ---
load_dotenv()
app = FastAPI()

origins = [
    
    "https://yt-shorts-maker-t1fy.onrender.com",
    "https://yt-shorts-maker.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

speech_key=os.getenv('SPEECH_KEY')
service_region=os.getenv('SERVICE_REGION')


if not speech_key:
    raise ValueError("Speech Key not available TATA")

# --- Main API Endpoint ---
@app.post('/api/voice')
async def process_video_endpoint(request: Request):
    words=[]

    def on_word_boundary(evt: speechsdk.SpeechSynthesisWordBoundaryEventArgs):
            timestamp_ms = ((evt.audio_offset + 5000) / 10000)
            word = evt.text
            end=(evt.duration.total_seconds()*1000) + timestamp_ms
            words.append({'word':word,'start':timestamp_ms,'end':end})
            print(f"WORD: '{word}', TIMESTAMP: {timestamp_ms:.2f} ms, END: {end}")
    try:
        response_data = await request.json()
        message = response_data.get('message')
        video_filename_id = response_data.get('video')

        if not message or not video_filename_id:
            raise HTTPException(status_code=400, detail="Missing 'message' or 'video' in request.")

        # --- OPTIMIZATION 1: Stream video directly from the URL ---
        # We no longer download the video first. We build the URL for FFmpeg.
        CLOUDINARY_BASE_URL = "https://res.cloudinary.com/dx2wns9yn/video/upload/"
        video_url = f"{CLOUDINARY_BASE_URL}{video_filename_id}"
        
        # --- Continue with audio generation ---


        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_voice_name= "hi-IN-MadhurNeural"
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
        )
        audio_output = speechsdk.audio.AudioOutputConfig(filename="output.mp3")

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_output
        )


        speech_synthesizer.synthesis_word_boundary.connect(on_word_boundary)

        result = speech_synthesizer.speak_text_async(message).get()


        data_json=words

        for i in data_json:    
            i['start']=i['start']/1000
            i['end']=i['end']/1000


        # audio_data = speech_api.speech(
        #     text=message, voice_id="Will", timestamp_type="word", bitrate="192k", pitch=1
        # )

        
        # audio_content = requests.get(audio_data['OutputUri']).content
        # timestamp_content = requests.get(audio_data['TimestampsUri']).content

        # temp_audio_path = 'temp_audio.mp3'
        # with open(temp_audio_path, 'wb') as file:
        #     file.write(audio_content)

        phrases = group_words_into_phrases(data_json)

        output_video_path = 'output.mp4'

        # Pass the URL directly to the generation function
        generate_video_with_text(
            input_url=video_url, # Pass the URL instead of a file path
            audio_file='output.mp3',
            output_file=output_video_path,
            data_json=data_json,
            phrases=phrases
        )

        return FileResponse(output_video_path, media_type='video/mp4', filename='generated_video.mp4')

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process video on server: {str(e)}")

# --- Helper functions ---
def group_words_into_phrases(words, max_words_per_phrase=3):
    if not words: return []
    phrases, current_phrase, phrase_start_time = [], [], words[0]["start"]
    for i, w in enumerate(words):
        current_phrase.append(w["word"])
        is_last_word = i == len(words) - 1
        ends_with_punctuation = any(c in w["word"] for c in ",.?!")
        if len(current_phrase) >= max_words_per_phrase or ends_with_punctuation or is_last_word:
            phrases.append({"phrase": " ".join(current_phrase), "start": phrase_start_time, "end": w["end"]})
            current_phrase = []
            if not is_last_word: phrase_start_time = words[i + 1]["start"]
    return phrases

def add_timed_text(stream, text, start, end, max_font_ratio=0.08, min_font_ratio=0.05,
                   fontcolor="white", outline=6):
    font_ratio = max(min_font_ratio, max_font_ratio - (len(text) / 50) * 0.01)
    font_file_path = "IMPACT.TTF" 
    return stream.drawtext(
        text=text, fontfile=font_file_path, fontsize=f"w*{font_ratio}", fontcolor=fontcolor,
        x="(w-text_w)/2", y="(h-text_h)/2", borderw=outline, bordercolor="black", box=0,
        enable=f"between(t,{start},{end})"
    )

def overlay_text_on_video(stream, phrases):
    for p in phrases:
        stream = add_timed_text(stream, p["phrase"], p["start"], p["end"])
    return stream

# Updated function to accept a URL
def generate_video_with_text(input_url, audio_file, output_file, data_json, phrases):
    if not data_json: raise ValueError("Timestamp data is empty.")
    audio_duration = data_json[-1]['end'] + 0.5
    
    # Use the input_url directly here
    input_video_stream = ffmpeg.input(input_url, stream_loop=-1, t=audio_duration).video
    input_audio_stream = ffmpeg.input(audio_file).audio
    
    video_with_text = overlay_text_on_video(input_video_stream, phrases)
    
    # --- OPTIMIZATION 2: Use a faster, less memory-intensive preset ---
    (ffmpeg.output(
        video_with_text, 
        input_audio_stream, 
        output_file, 
        vcodec='libx264', 
        acodec='aac', 
        strict='experimental',
        preset='ultrafast' # Add this preset
    ).overwrite_output().run())


