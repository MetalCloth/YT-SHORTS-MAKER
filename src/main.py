import os
import json
import requests
import ffmpeg
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from unrealspeech import UnrealSpeechAPI

# --- Initialization ---
load_dotenv()
app = FastAPI()

# IMPORTANT: Configure this more securely for a real production environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key and initialize the speech API
api_key = os.getenv("UNREAL_SPEECH_API_KEY")
if not api_key:
    raise ValueError("UNREAL_SPEECH_API_KEY not found in environment variables.")
speech_api = UnrealSpeechAPI(api_key)


# --- Main API Endpoint ---
@app.post('/api/voice')
async def process_video_endpoint(request: Request):
    try:
        response_data = await request.json()
        message = response_data.get('message')
        video_filename = response_data.get('video')

        if not message or not video_filename:
            raise HTTPException(status_code=400, detail="Missing 'message' or 'video' in request.")

        # --- All processing logic is now inside this single function ---

        # 1. Generate audio from the message
        audio_data = speech_api.speech(
            text=message,
            voice_id="Will",
            timestamp_type="word",
            bitrate="192k",
            pitch=1
        )

        # 2. Download audio and timestamp files
        audio_content = requests.get(audio_data['OutputUri']).content
        timestamp_content = requests.get(audio_data['TimestampsUri']).content

        # 3. Save the downloaded audio to a temporary file
        temp_audio_path = 'temp_audio.mp3'
        with open(temp_audio_path, 'wb') as file:
            file.write(audio_content)

        # 4. Process timestamps and group words into phrases
        data_json = json.loads(timestamp_content.decode("utf-8"))
        phrases = group_words_into_phrases(data_json)

        # 5. Define input video path and final output path
        input_video_path = f"video_templates/{video_filename}"
        output_video_path = 'output.mp4'

        # 6. Run the ffmpeg function to combine video, audio, and text
        generate_video_with_text(
            input_file=input_video_path,
            audio_file=temp_audio_path,
            output_file=output_video_path,
            data_json=data_json,
            phrases=phrases
        )

        # 7. Return the generated video file
        return FileResponse(output_video_path, media_type='video/mp4', filename='generated_video.mp4')

    except Exception as e:
        print(f"An error occurred: {e}")
        # Return a JSON error response
        raise HTTPException(status_code=500, detail=f"Failed to process video on server: {e}")


# --- Helper Functions ---

def group_words_into_phrases(words, max_words_per_phrase=3):
    """Groups individual words into phrases based on punctuation or max word count."""
    if not words:
        return []
        
    phrases = []
    current_phrase = []
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


def add_timed_text(stream, text, start, end):
    """Adds centered, auto-shrinking text overlay to the video stream."""
    max_font_ratio = 0.08
    min_font_ratio = 0.05
    font_ratio = max(min_font_ratio, max_font_ratio - (len(text) / 50) * 0.01)

    return stream.drawtext(
        text=text,
        # IMPORTANT: Make sure 'impact.ttf' is in the same directory as your main.py
        fontfile="impact.ttf",
        fontsize=f"w*{font_ratio}",
        fontcolor="white",
        x="(w-text_w)/2",
        y="(h-text_h)/2",
        borderw=6,
        bordercolor="black",
        enable=f"between(t,{start},{end})"
    )


def overlay_text_on_video(stream, phrases):
    """Applies all timed phrases to the video stream."""
    for p in phrases:
        stream = add_timed_text(stream, p["phrase"], p["start"], p["end"])
    return stream


def generate_video_with_text(input_file, audio_file, output_file, data_json, phrases):
    """Main ffmpeg processing function."""
    if not data_json:
        raise ValueError("Timestamp data is empty, cannot determine audio duration.")

    audio_duration = data_json[-1]['end'] + 0.5

    input_video_stream = ffmpeg.input(input_file, stream_loop=-1, t=audio_duration).video
    input_audio_stream = ffmpeg.input(audio_file).audio

    video_with_text = overlay_text_on_video(input_video_stream, phrases)

    (
        ffmpeg
        .output(video_with_text, input_audio_stream, output_file, vcodec='libx264', acodec='aac', strict='experimental')
        .overwrite_output()
        .run()
    )