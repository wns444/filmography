import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { filmsAPI, commentsAPI } from '../api/client'
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

const MessageIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
  </svg>
)

export default function FilmDetail() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const [film, setFilm] = useState(null)
  const [comments, setComments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [liked, setLiked] = useState(false)

  useEffect(() => {
    const fetchFilm = async () => {
      try {
        setLoading(true)
        const res = await filmsAPI.getBySlug(slug)
        setFilm(res.data)
        
        // Fetch comments if film has an ID
        if (res.data.id) {
          try {
            const commentsRes = await commentsAPI.getFilmComments(res.data.id)
            setComments(commentsRes.data)
          } catch (err) {
            console.log('Комментарии недоступны')
          }
        }
      } catch (err) {
        setError('Фильм не найден')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchFilm()
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

  if (!film) return null

  return (
    <div className="space-y-8 pb-12">
      {/* Hero Section */}
      <div className="relative w-full h-96 md:h-[500px] bg-netflix-gray overflow-hidden rounded-lg">
        <div className="absolute inset-0 bg-gradient-to-r from-netflix-dark via-transparent to-netflix-dark z-10" />
        <div className="absolute inset-0 flex items-center justify-center text-gray-600">
          🎬 {film.category}
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
          <h1 className="text-4xl md:text-5xl font-bold mb-4">{film.name}</h1>
          
          <div className="flex flex-wrap items-center gap-4 mb-6">
            <span className="px-3 py-1 bg-netflix-accent/20 text-netflix-accent rounded font-semibold">
              {film.category}
            </span>
            {film.rating && (
              <div className="flex items-center space-x-2">
                <span className="text-yellow-400 font-bold">⭐ {film.rating.toFixed(1)}</span>
                <span className="text-gray-400">/10</span>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-4 mb-8">
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
          </div>
        </div>

        {/* Description */}
        <div className="bg-netflix-light rounded-lg p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">О фильме</h2>
          <p className="text-gray-300 leading-relaxed">
            {film.description || 'Описание недоступно'}
          </p>
        </div>

        {/* Comments Section */}
        <div className="bg-netflix-light rounded-lg p-6">
          <div className="flex items-center space-x-2 mb-6">
            <div className="text-netflix-accent">
              <MessageIcon />
            </div>
            <h2 className="text-xl font-bold">Комментарии ({comments.length})</h2>
          </div>

          {comments.length > 0 ? (
            <div className="space-y-4">
              {comments.slice(0, 5).map(comment => (
                <div key={comment.id} className="border-l-2 border-netflix-accent pl-4 py-2">
                  <p className="font-semibold text-sm text-gray-400">{comment.user?.username || 'Аноним'}</p>
                  <p className="text-gray-300 mt-1">{comment.text}</p>
                  <p className="text-xs text-gray-500 mt-2">
                    {new Date(comment.created_at).toLocaleDateString('ru-RU')}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-400 text-center py-8">Комментариев еще нет</p>
          )}
        </div>
      </div>
    </div>
  )
}
