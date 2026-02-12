import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import FilmCard from '../components/FilmCard'
import LoadingSpinner from '../components/LoadingSpinner'
import { filmsAPI } from '../api/client'

const FilterIcon = () => <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
const XIcon = () => <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>

export default function Films() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [films, setFilms] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState({
    category: '',
    minRating: '',
  })

  const searchQuery = searchParams.get('search') || ''

  useEffect(() => {
    const fetchFilms = async () => {
      try {
        setLoading(true)
        const query = {
          ...(searchQuery && { name: searchQuery }),
          ...(filters.category && { category: filters.category }),
          ...(filters.minRating && { rating: parseInt(filters.minRating) }),
        }
        const res = await filmsAPI.search(query)
        setFilms(res.data)
      } catch (err) {
        setError('Ошибка загрузки фильмов')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchFilms()
  }, [searchQuery, filters])

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const clearFilters = () => {
    setFilters({ category: '', minRating: '' })
  }

  return (
    <div className="px-4 md:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">
          {searchQuery ? `Поиск: "${searchQuery}"` : 'Все фильмы'}
        </h1>
        <p className="text-gray-400">Найдено фильмов: {films.length}</p>
      </div>

      {/* Content */}
      {loading ? (
        <LoadingSpinner />
      ) : error ? (
        <div className="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded">
          {error}
        </div>
      ) : films.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          {films.map(film => (
            <FilmCard key={film.id} film={film} type="film" />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-400 text-lg">Фильмы не найдены</p>
          <p className="text-gray-500 mt-2">Попробуйте изменить фильтры</p>
        </div>
      )}
    </div>
  )
}
