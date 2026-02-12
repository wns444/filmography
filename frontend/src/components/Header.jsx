import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const SearchIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="11" cy="11" r="8"></circle>
    <path d="m21 21-4.35-4.35"></path>
  </svg>
)

const MenuIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="3" y1="6" x2="21" y2="6"></line>
    <line x1="3" y1="12" x2="21" y2="12"></line>
    <line x1="3" y1="18" x2="21" y2="18"></line>
  </svg>
)

const XIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="18" y1="6" x2="6" y2="18"></line>
    <line x1="6" y1="6" x2="18" y2="18"></line>
  </svg>
)

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/films?search=${searchQuery}`)
    }
  }

  return (
    <header className="sticky top-0 z-50 bg-gradient-to-b from-netflix-dark via-netflix-gray to-transparent border-b border-netflix-light">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <span className="text-xl font-bold hidden sm:inline group-hover:text-netflix-accent transition">Filmography</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link to="/" className="hover:text-netflix-accent transition duration-200">
              Главная
            </Link>
            <Link to="/films" className="hover:text-netflix-accent transition duration-200">
              Фильмы
            </Link>
            <Link to="/serials" className="hover:text-netflix-accent transition duration-200">
              Сериалы
            </Link>
          </nav>

          {/* Search */}
          <form onSubmit={handleSearch} className="hidden md:flex items-center bg-netflix-light rounded-full px-4 py-2 focus-within:ring-2 focus-within:ring-netflix-accent">
            <input
              type="text"
              placeholder="Поиск..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-transparent outline-none text-sm flex-grow placeholder-gray-500"
            />
            <button type="submit" className="text-gray-400 hover:text-netflix-accent transition">
              <SearchIcon />
            </button>
          </form>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 hover:bg-netflix-light rounded transition"
          >
            {mobileMenuOpen ? <XIcon /> : <MenuIcon />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <nav className="md:hidden mt-4 space-y-3 pb-4">
            <Link to="/" className="block py-2 hover:text-netflix-accent transition">
              Главная
            </Link>
            <Link to="/films" className="block py-2 hover:text-netflix-accent transition">
              Фильмы
            </Link>
            <Link to="/serials" className="block py-2 hover:text-netflix-accent transition">
              Сериалы
            </Link>
            <form onSubmit={handleSearch} className="flex items-center bg-netflix-light rounded-lg px-3 py-2 mt-3">
              <input
                type="text"
                placeholder="Поиск..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-transparent outline-none text-sm flex-grow placeholder-gray-500"
              />
              <button type="submit" className="text-gray-400 hover:text-netflix-accent">
                <Search size={18} />
              </button>
            </form>
          </nav>
        )}
      </div>
    </header>
  )
}
