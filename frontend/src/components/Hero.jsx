const PlayIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <path d="M5 3l14 9-14 9V3z"/>
  </svg>
)

const VolumeOffIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
    <line x1="23" y1="9" x2="17" y2="15"></line>
    <line x1="17" y1="9" x2="23" y2="15"></line>
  </svg>
)

const VolumeIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
    <path d="M15.54 5.47A9 9 0 0 1 19 9"></path>
    <path d="M15.07 19.07A9 9 0 0 1 5 9"></path>
  </svg>
)

import { useState } from 'react'

export default function Hero({ content }) {
  const [muted, setMuted] = useState(true)

  if (!content) {
    return (
      <div className="w-full h-96 bg-netflix-gray rounded-lg flex items-center justify-center">
        <p className="text-gray-400">Контент недоступен</p>
      </div>
    )
  }

  return (
    <div className="relative w-full h-96 rounded-lg overflow-hidden group">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-r from-netflix-dark via-black to-transparent z-10" />
      
      {/* Backdrop */}
      <div className="absolute inset-0">
        <div className="w-full h-full bg-gradient-to-br from-netflix-light to-black flex items-center justify-center">
          <div className="text-center text-gray-600">
            <p className="text-lg">🎬 {content.category}</p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="absolute inset-0 flex flex-col justify-end p-8 z-20">
        <h1 className="text-4xl md:text-5xl font-bold mb-4 max-w-2xl">{content.name}</h1>
        
        <p className="text-gray-300 max-w-xl mb-6 line-clamp-3">
          {content.description || 'Необыкновенная история, которая изменит вашу жизнь'}
        </p>

        {/* Rating */}
        {content.rating && (
          <div className="flex items-center space-x-4 mb-6">
            <div className="bg-netflix-accent/20 text-netflix-accent px-4 py-2 rounded font-bold">
              ⭐ {content.rating.toFixed(1)}/10
            </div>
            <span className="text-gray-400">{content.category}</span>
          </div>
        )}

        {/* Buttons */}
        {/* <div className="flex items-center space-x-4">
          <button className="bg-netflix-accent hover:bg-red-700 text-white font-bold py-3 px-8 rounded flex items-center space-x-2 transition duration-200 hover:scale-105">
            <PlayIcon />
            <span>Смотреть</span>
          </button>
          <button
            onClick={() => setMuted(!muted)}
            className="bg-white/20 hover:bg-white/30 text-white font-bold py-3 px-4 rounded transition duration-200"
          >
            {muted ? <VolumeOffIcon /> : <VolumeIcon />}
          </button>
        </div> */}
      </div>
    </div>
  )
}
