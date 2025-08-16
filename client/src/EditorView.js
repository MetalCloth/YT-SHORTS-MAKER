import React, { useState, useRef } from 'react';

const EditorView = ({ videoObject, onGoBack, setGenerating }) => {
  const videoRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);
  const [text, setText] = useState('');

  const handleVideoClick = () => {
    if (videoRef.current?.paused) {
      videoRef.current.play();
    } else {
      videoRef.current?.pause();
    }
  };

  const handleSubmit = async () => {
    if (!text.trim()) {
      alert('Please write something before submitting!');
      return;
    }
    setIsLoading(true);
    setGenerating(true);

    try {
      // Use the environment variable to find the backend API
      const apiUrl = process.env.REACT_APP_API_URL;
      const response = await fetch(`${apiUrl}/api/voice`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text, video: videoObject.filename }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || `Server error: ${response.status}`;
        throw new Error(errorMessage);
      }

      console.log("Video generated successfully. Preparing for download...");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'generated-video.mp4';
      document.body.appendChild(a);
      a.click();
      
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (error) {
      console.error("Error during video processing:", error);
      alert(`Failed to process video. Reason: ${error.message}`);
    } finally {
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
              src={videoObject.url}
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

export default EditorView;