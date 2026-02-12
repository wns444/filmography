import { useEffect, useState } from 'react'
import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay, Pagination, Navigation } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';
import Hero from '../components/Hero'
import FilmCard from '../components/FilmCard'
import LoadingSpinner from '../components/LoadingSpinner'
import { filmsAPI, serialsAPI } from '../api/client'

const TrendingIcon = () => <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="23" y1="6"></line><polyline points="13 20 21 12 21 4 3 4 21 20"></polyline></svg>
const EyeIcon = () => <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>

export default function Home() {
	const [topFilms, setTopFilms] = useState([])
	const [topSerials, setTopSerials] = useState([])
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState(null)

	useEffect(() => {
		const fetchData = async () => {
			try {
				setLoading(true)
				const [filmsRes, serialsRes] = await Promise.all([
					filmsAPI.getAll(10),
					serialsAPI.getAll(10)
				])
				setTopFilms(filmsRes.data)
				setTopSerials(serialsRes.data)
			} catch (err) {
				setError('Ошибка загрузки данных')
				console.error(err)
			} finally {
				setLoading(false)
			}
		}

		fetchData()
	}, [])

	if (loading) {
		return <LoadingSpinner />
	}

	return (
		<div className="space-y-12 pb-12">

			{/* Hero Section */}
			<section className="px-4 md:px-6 lg:px-8 pt-8">
				<Swiper
					modules={[Autoplay, Pagination, Navigation]}
					spaceBetween={30}
					slidesPerView={1}
					autoplay={{
						delay: 5000,
						disableOnInteraction: false,
					}}
					pagination={{ clickable: true }}
					navigation
					loop={true}
					className="hero-slider"
				>
					{topFilms.map((film) => (
						<SwiperSlide key={film.id}>
							<Hero content={film} />
						</SwiperSlide>
					))}
				</Swiper>
			</section>

			{/* Trending Films Section */}
			<section className="px-4 md:px-6 lg:px-8">
				<div className="text-netflix-accent flex items-center space-x-2 mb-6">
					<TrendingIcon />
					<h2 className="text-2xl md:text-3xl font-bold">Популярные фильмы</h2>
				</div>
				{topFilms.length > 0 ? (
					<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
						{topFilms.slice(0, 10).map(film => (
							<FilmCard key={film.id} film={film} type="film" />
						))}
					</div>
				) : (
					<p className="text-gray-400 text-center py-8">Фильмы не найдены</p>
				)}
			</section>

			{/* Top Serials Section */}
			<section className="px-4 md:px-6 lg:px-8">
				<div className="flex items-center space-x-2 mb-6">
					<div className="text-netflix-accent"><EyeIcon /></div>
					<h2 className="text-2xl md:text-3xl font-bold">Топ сериалов</h2>
				</div>
				{topSerials.length > 0 ? (
					<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
						{topSerials.slice(0, 10).map(serial => (
							<FilmCard key={serial.id} film={serial} type="serial" />
						))}
					</div>
				) : (
					<p className="text-gray-400 text-center py-8">Сериалы не найдены</p>
				)}
			</section>

			{error && (
				<div className="px-4 md:px-6 lg:px-8">
					<div className="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded">
						{error}
					</div>
				</div>
			)}
		</div>
	)
}
