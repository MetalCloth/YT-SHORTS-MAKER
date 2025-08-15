// src/App.js
import React, { useState } from 'react';
import VideoCard from './VideoCard';
import EditorView from './EditorView';
import './App.css';

const videoData = [
  'https://github.com/user-attachments/assets/17b8cd7f-88e4-43b1-a46a-e02f84b341f2',
  'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
  'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
  'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
  'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
  'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
  'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4'
];

function App() {
  const [currentView, setCurrentView] = useState('grid');
  const [selectedVideo, setSelectedVideo] = useState(null);

  const handleCardClick = (videoUrl) => {
    setSelectedVideo(videoUrl);
    setCurrentView('editor');
  };

  const handleGoBack = () => {
    setSelectedVideo(null);
    setCurrentView('grid');
  };

  return (
    <div className="container">
      {currentView === 'grid' ? (
        <>
          <div className="header">
            <h1>Templates</h1>
            <p className="subtitle">Professional video templates for content creators</p>
          </div>
          <div className="templates-grid">
            {videoData.map((url, index) => (
              <VideoCard
                key={index}
                videoSrc={url}
                onClick={handleCardClick}
              />
            ))}
          </div>
        </>
      ) : (
        <EditorView videoSrc={selectedVideo} onGoBack={handleGoBack} />
      )}
    </div>
  );
}

export default App;