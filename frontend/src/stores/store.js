import { create } from 'zustand'

export const useStore = create((set) => ({
  films: [],
  serials: [],
  selectedFilm: null,
  selectedSerial: null,
  loading: false,
  error: null,
  searchQuery: '',
  
  setFilms: (films) => set({ films }),
  setSerials: (serials) => set({ serials }),
  setSelectedFilm: (film) => set({ selectedFilm: film }),
  setSelectedSerial: (serial) => set({ selectedSerial: serial }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  setSearchQuery: (query) => set({ searchQuery: query }),
}))
