import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { serialsAPI } from '../api/client'
import LoadingSpinner from '../components/LoadingSpinner'

const ArrowLeftIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M19 12H5M12 19l-7-7 7-7"/>
  </svg>
)

const PlayIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <path d="M5 3l14 9-14 9V3z"/>
  </svg>
)

const HeartIcon = ({ filled }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill={filled ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2">
    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
  </svg>
)

const ShareIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="18" cy="5" r="3"/>
    <circle cx="6" cy="12" r="3"/>
    <circle cx="18" cy="19" r="3"/>
    <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
    <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
  </svg>
)

const ChevronDownIcon = ({ expanded }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={`transition-transform ${expanded ? 'rotate-180' : ''}`}>
    <polyline points="6 9 12 15 18 9"></polyline>
  </svg>
)

export default function SerialDetail() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const [serial, setSerial] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [liked, setLiked] = useState(false)
  const [expandedSeason, setExpandedSeason] = useState(null)

  useEffect(() => {
    const fetchSerial = async () => {
      try {
        setLoading(true)
        const res = await serialsAPI.getBySlug(slug)
        setSerial(res.data)
      } catch (err) {
        setError('Сериал не найден')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchSerial()
  }, [slug])

  if (loading) return <LoadingSpinner />

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-4">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">{error}</h1>
          <button
            onClick={() => navigate('/')}
            className="bg-netflix-accent hover:bg-red-700 text-white font-bold py-2 px-6 rounded transition"
          >
            На главную
          </button>
        </div>
      </div>
    )
  }

  if (!serial) return null

  return (
    <div className="space-y-8 pb-12">
      {/* Hero Section */}
      <div className="relative w-full h-96 md:h-[500px] bg-netflix-gray overflow-hidden rounded-lg">
        <div className="absolute inset-0 bg-gradient-to-r from-netflix-dark via-transparent to-netflix-dark z-10" />
        <div className="absolute inset-0 flex items-center justify-center text-gray-600">
          🎬 {serial.category}
        </div>
      </div>

      <div className="px-4 md:px-6 lg:px-8 max-w-5xl mx-auto w-full">
        {/* Back Button */}
        <button
          onClick={() => navigate(-1)}
          className="flex items-center space-x-2 text-gray-400 hover:text-netflix-accent transition mb-6"
        >
          <ArrowLeftIcon />
          <span>Назад</span>
        </button>

        {/* Title and Meta */}
        <div className="mb-8">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">{serial.name}</h1>
          
          <div className="flex flex-wrap items-center gap-4 mb-6">
            <span className="px-3 py-1 bg-netflix-accent/20 text-netflix-accent rounded font-semibold">
              {serial.category}
            </span>
            {serial.rating && (
              <div className="flex items-center space-x-2">
                <span className="text-yellow-400 font-bold">⭐ {serial.rating.toFixed(1)}</span>
                <span className="text-gray-400">/10</span>
              </div>
            )}
            <span className="text-gray-400">
              {serial.seasons?.length || 0} сезонов
            </span>
          </div>

          {/* Action Buttons */}
          {/* <div className="flex flex-wrap gap-4 mb-8">
            <button className="bg-netflix-accent hover:bg-red-700 text-white font-bold py-3 px-8 rounded flex items-center space-x-2 transition duration-200 hover:scale-105">
              <PlayIcon />
              <span>Смотреть</span>
            </button>
            <button
              onClick={() => setLiked(!liked)}
              className={`font-bold py-3 px-6 rounded flex items-center space-x-2 transition duration-200 ${
                liked
                  ? 'bg-netflix-accent/30 text-netflix-accent'
                  : 'bg-white/10 hover:bg-white/20 text-white'
              }`}
            >
              <HeartIcon filled={liked} />
              <span>{liked ? 'Нравится' : 'В список'}</span>
            </button>
            <button className="bg-white/10 hover:bg-white/20 text-white font-bold py-3 px-6 rounded flex items-center space-x-2 transition duration-200">
              <ShareIcon />
              <span>Поделиться</span>
            </button>
          </div> */}
        </div>

        {/* Description */}
        <div className="bg-netflix-light rounded-lg p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">О сериале</h2>
          <p className="text-gray-300 leading-relaxed">
            {serial.description || 'Описание недоступно'}
          </p>
        </div>

        {/* Seasons Section */}
        {serial.seasons && serial.seasons.length > 0 && (
          <div className="bg-netflix-light rounded-lg overflow-hidden">
            <h2 className="text-xl font-bold p-6 border-b border-netflix-gray">
              Сезоны ({serial.seasons.length})
            </h2>
            <div className="space-y-2 p-6">
              {serial.seasons.map(season => (
                <div key={season.id} className="border border-netflix-gray rounded-lg overflow-hidden">
                  <button
                    onClick={() => setExpandedSeason(
                      expandedSeason === season.id ? null : season.id
                    )}
                    className="w-full flex items-center justify-between p-4 hover:bg-netflix-gray transition"
                  >
                    <div className="text-left">
                      <h3 className="font-bold text-lg">
                        Сезон {season.number} {season.name && `- ${season.name}`}
                      </h3>
                      {season.description && (
                        <p className="text-sm text-gray-400 mt-1">{season.description}</p>
                      )}
                    </div>
                    <ChevronDownIcon expanded={expandedSeason === season.id} />
                  </button>

                  {/* Episodes */}
                  {expandedSeason === season.id && season.chapters && (
                    <div className="bg-netflix-gray px-4 py-3 space-y-2">
                      {season.chapters.map(chapter => (
                        <div
                          key={chapter.id}
                          className="flex items-center space-x-3 p-3 hover:bg-netflix-light rounded transition cursor-pointer group"
                        >
                          <div className="flex-shrink-0 w-10 h-10 bg-netflix-light rounded flex items-center justify-center font-bold text-sm group-hover:bg-netflix-accent/20 transition">
                            {chapter.number}
                          </div>
                          <div className="flex-grow">
                            <p className="font-semibold">{chapter.name || `Эпизод ${chapter.number}`}</p>
                            {chapter.description && (
                              <p className="text-xs text-gray-400">{chapter.description}</p>
                            )}
                          </div>
                          {/* <Play
                            size={18}
                            className="text-gray-400 group-hover:text-netflix-accent transition"
                            fill="currentColor"
                          /> */}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
