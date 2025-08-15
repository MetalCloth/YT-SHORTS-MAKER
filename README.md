# AutoShorts 🚀 - AI-Powered Shorts & Reels Creator



Stop spending hours editing. **AutoShorts** is a powerful tool that transforms your text into engaging, ready-to-post vertical videos for YouTube Shorts, Instagram Reels, and TikTok. Simply choose a template, type your script, and let the AI handle the voice-over and synchronized captions.

---

## Example
* **Before**:
 https://github.com/user-attachments/assets/1a53ee48-60af-494e-b8a7-2c0c1301bca2

* **Prompt**:
  
* **Output**:
  https://github.com/user-attachments/assets/46b975e5-2262-4b04-b1b1-d193c9c95485




  


## ✨ Features

* **Automated Workflow:** Go from a simple text script to a downloadable video in seconds.
* **AI Voice Generation:** Leverages the UnrealSpeech API for high-quality, realistic text-to-speech voice-overs.
* **Synchronized Captions:** Uses FFmpeg to automatically generate and burn word-level subtitles into the video, perfectly synced with the audio.
* **Template-Based Creation:** Select from a grid of video templates to get started quickly.
* **Interactive UI:** A sleek and responsive React interface with loading states and a full-page blur effect during video generation.
* **Direct Downloads:** Your final video is downloaded directly in your browser.

---

## 🛠️ Tech Stack

### Frontend
* **Framework:** React
* **Language:** JavaScript (ES6+)
* **Styling:** CSS

### Backend
* **Framework:** FastAPI
* **Language:** Python 3.8+
* **Video Processing:** FFmpeg
* **AI Voice API:** UnrealSpeech

---

## 🚀 Getting Started

Follow these steps to get AutoShorts running locally.

### Prerequisites

Make sure you have the following installed on your system:
* **Node.js** (v16 or later) and **npm**
* **Python** (v3.8 or later)
* **FFmpeg:** This is a **critical** dependency. You must install it from the [official FFmpeg website](https://ffmpeg.org/download.html) and ensure it's accessible from your system's command line.

### Backend Setup

1.  Navigate to your backend directory.
2.  Create and activate a Python virtual environment:
    ```bash
    # Create the environment
    python -m venv venv

    # Activate on Windows: .\venv\Scripts\activate
    # Activate on Mac/Linux: source venv/bin/activate
    ```
3.  Install the required Python packages:
    ```bash
    pip install fastapi "uvicorn[standard]" python-dotenv unrealspeech requests ffmpeg-python python-multipart
    ```
4.  Create a `.env` file in the backend directory and add your API key:
    ```
    UNREAL_SPEECH_API_KEY="your_unrealspeech_api_key_here"
    ```

### Frontend Setup

1.  Navigate to your frontend directory.
2.  Install the necessary npm packages:
    ```bash
    npm install
    ```

---

## ▶️ Usage

You must have **both** the backend and frontend servers running in separate terminals.

**1. Start the Backend Server:**
```bash
# In the backend directory (with venv active)
uvicorn main:app --reload
