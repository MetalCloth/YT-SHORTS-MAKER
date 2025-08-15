// src/EditorView.js
import React, { useState, useRef } from 'react';

const EditorView = ({ videoSrc, onGoBack }) => {
  const videoRef = useRef(null);
  const [text, setText] = useState('');

  const handleVideoClick = () => {
    if (videoRef.current && videoRef.current.paused) {
      videoRef.current.play();
    } else if (videoRef.current) {
      videoRef.current.pause();
    }
  };

  const handleSubmit = async () => {
  if (!text.trim()) {
    alert('Please write something before submitting!');
    return;
  }

  try {
    // Make POST request to FastAPI backend
    const res = await fetch("http://localhost:8000/api/voice", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: text }), // Send actual text
    });

    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }

    const data = await res.json();
    console.log("Message sent! Backend says:", data.message);
    alert(`Message sent! Backend says: ${data.message}`);

  } catch (error) {
    console.error("Error sending text:", error);
    alert("Failed to send text to backend.");
  }
};

  return (
    <div className="editor-view">
      <button className="back-btn" onClick={onGoBack}>← Back to Templates</button>
      <div className="editor-content">
        <div className="video-preview">
          <div className="video-container">
            <video
              ref={videoRef}
              className="video-player"
              src={videoSrc}
              onClick={handleVideoClick}
              autoPlay
              loop
              muted
              playsInline
            />
          </div>
        </div>
        <div className="controls-panel">
          <div className="control-group">
            <label className="control-label">Text Content</label>
            <textarea
              className="text-input"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter your message..."
            ></textarea>
          </div>
          <button className="submit-btn" onClick={handleSubmit}>
            Generate Video
          </button>
        </div>
      </div>
    </div>
  );
};

export default EditorView;