import { Link } from 'react-router-dom'

const StarIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
    <polygon points="12 2 15.09 10.26 24 10.26 17.55 15.75 19.64 24 12 19.51 4.36 24 6.45 15.75 0 10.26 8.91 10.26 12 2"></polygon>
  </svg>
)

const PlayIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M5 3l14 9-14 9V3z"/>
  </svg>
)

export default function FilmCard({ film, type = 'film' }) {
  const href = type === 'film' ? `/films/${film.slug}` : `/serials/${film.slug}`
  
  return (
    <Link to={href}>
      <div className="group relative overflow-hidden rounded-lg bg-netflix-light card-hover cursor-pointer h-80">
        {/* Placeholder Image Background */}
        <div className="w-full h-full bg-gradient-to-br from-netflix-light to-black relative overflow-hidden">
          {film.poster_url ? (
            <img
              src={film.poster_url}
              alt={film.name}
              className="w-full h-full object-cover group-hover:scale-110 transition duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-netflix-light">
              <div className="text-center text-gray-600">
                <div className="mx-auto mb-2 opacity-50 flex justify-center">
                  <PlayIcon />
                </div>
                <p className="text-xs">Изображение недоступно</p>
              </div>
            </div>
          )}
          
          {/* Dark Overlay */}
          <div className="absolute inset-0 bg-black/60 group-hover:bg-black/40 transition duration-300" />
        </div>

        {/* Content */}
        <div className="absolute inset-0 flex flex-col justify-end p-4 translate-y-12 group-hover:translate-y-0 transition duration-300">
          <h3 className="font-bold text-lg truncate">{film.name}</h3>
          
          {/* Category and Rating */}
          <div className="flex items-center justify-between mt-2 mb-3">
            <span className="text-xs bg-netflix-accent/20 text-netflix-accent px-2 py-1 rounded">
              {film.category}
            </span>
            {film.rating && (
              <div className="flex items-center space-x-1 text-yellow-400">
                <StarIcon />
                <span className="text-sm font-semibold">{film.rating.toFixed(1)}</span>
              </div>
            )}
          </div>

          {/* Description */}
          <p className="text-xs text-gray-300 line-clamp-2 mb-3">
            {film.description || 'Описание недоступно'}
          </p>

          {/* Watch Button */}
          {/* <button className="bg-netflix-accent hover:bg-red-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center space-x-2 transition duration-200 w-full">
            <PlayIcon />
            <span>Смотреть</span>
          </button> */}
        </div>
      </div>
    </Link>
  )
}
