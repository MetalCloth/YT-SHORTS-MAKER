// src/EditorView.js
import React, { useState, useRef } from 'react';

const EditorView = ({ videoSrc, onGoBack, setGenerating }) => {
  const videoRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);
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
    setIsLoading(true);
    setGenerating(true); // Activate blur and block feature

    try {
      // Step 1: Your original POST request to send the data and queue the job.
      const postRes = await fetch("http://localhost:8000/api/voice", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text, video: videoSrc }),
      });

      if (!postRes.ok) {
        throw new Error(`Data submission failed: ${postRes.status}`);
      }
      console.log("Data sent. Now generating and fetching the video...");

      // Step 2: Immediately make a GET request to trigger generation and receive the file.
      const getRes = await fetch("http://localhost:8000/api/voice");
      
      if (!getRes.ok) {
        throw new Error(`Video generation failed: ${getRes.status}`);
      }

      // Step 3: Process the file response as a 'blob' to download it without navigation.
      const blob = await getRes.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'generated-video.mp4'; // Set the download filename
      document.body.appendChild(a);
      a.click(); // Trigger the download
      
      // Clean up by removing the temporary link and URL
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (error) {
      console.error("Error in process:", error);
      alert("Failed to process video. Please try again.");
    } finally {
      // Step 4: This 'finally' block will now run correctly.
      // It removes the spinner, blur, and block feature.
      setIsLoading(false);
      setGenerating(false);
    }
  };

  return (
    <div className="editor-view">
      <button className="back-btn" onClick={onGoBack} disabled={isLoading}>
        ← Back to Templates
      </button>
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
            {isLoading && (
              <div className="loading-overlay">
                <div className="spinner"></div>
              </div>
            )}
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
              disabled={isLoading}
            ></textarea>
          </div>
          <button className="submit-btn" onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? 'Generating...' : 'Generate Video'}
          </button>
        </div>
      </div>
    </div>
  );
};

export  default EditorView;