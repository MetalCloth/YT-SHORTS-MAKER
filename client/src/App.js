import React, { useState } from 'react';
import VideoCard from './VideoCard';
import EditorView from './EditorView';
import './App.css';

const videoData = [
  { url: '/video_templates/github_video_1.mp4', filename: 'github_video_1.mp4' },
  { url: '/video_templates/github_video_2.mp4', filename: 'github_video_2.mp4' },
  { url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', filename: 'BigBuckBunny.mp4' },
];

function App() {
  const [currentView, setCurrentView] = useState('grid');
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleCardClick = (videoObject) => {
    setSelectedVideo(videoObject);
    setCurrentView('editor');
  };

  const handleGoBack = () => {
    setSelectedVideo(null);
    setCurrentView('grid');
    setIsGenerating(false);
  };

  const setGeneratingState = (generating) => {
    setIsGenerating(generating);
  };
  
  if (isGenerating) {
    document.body.classList.add('blur-loading');
  } else {
    document.body.classList.remove('blur-loading');
  }

  return (
    <div className="container">
      {currentView === 'grid' ? (
        <>
          <div className="header">
            <h1>Templates</h1>
            <p className="subtitle">Professional video templates for content creators</p>
          </div>
          <div className="templates-grid">
            {videoData.map((video, index) => (
              <VideoCard
                key={index}
                videoSrc={video.url}
                onClick={() => handleCardClick(video)}
              />
            ))}
          </div>
        </>
      ) : (
        <EditorView
          videoObject={selectedVideo}
          onGoBack={handleGoBack}
          setGenerating={setGeneratingState}
        />
      )}
    </div>
  );
}

export default App;