import React, { useState } from 'react';
import VideoCard from './VideoCard';
import EditorView from './EditorView';
import './App.css';

/*
  args:
    url: the cloudinary url of the video
    filename: the filename of the video
*/
const videoData = [
  { 
    url: 'https://res.cloudinary.com/dx2wns9yn/video/upload/v1755359695/github_video_1_dcitx6.mp4', 
    filename: 'v1755359695/github_video_1_dcitx6.mp4' 
  },
  { 
    url: 'https://res.cloudinary.com/dx2wns9yn/video/upload/v1755359641/github_video_2_mkolsd.mp4',
    filename: 'v1755359641/github_video_2_mkolsd.mp4' 
  },
  { 
    url: 'https://res.cloudinary.com/dx2wns9yn/video/upload/v1755359640/BigBuckBunny_he2esq.mp4',
    filename: 'v1755359640/BigBuckBunny_he2esq.mp4'
  },
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
            <p className="subtitle">Video templates for content creators</p>
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
