// src/VideoCard.js
import React, { useRef } from 'react';

const VideoCard = ({ videoSrc, onClick }) => {
  const videoRef = useRef(null);

  const handleMouseEnter = () => {
    if (videoRef.current) {
      videoRef.current.play();
    }
  };

  const handleMouseLeave = () => {
    if (videoRef.current) {
      videoRef.current.pause();
      videoRef.current.currentTime = 0;
    }
  };

  return (
    <div
      className="template-card"
      onClick={() => onClick(videoSrc)}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <video
        ref={videoRef}
        className="template-video"
        muted
        loop
        playsInline
        src={videoSrc}
      />
    </div>
  );
};

export default VideoCard;