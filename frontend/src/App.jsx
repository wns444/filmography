import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Films from './pages/Films'
import Serials from './pages/Serials'
import FilmDetail from './pages/FilmDetail'
import SerialDetail from './pages/SerialDetail'

export default function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/films" element={<Films />} />
          <Route path="/serials" element={<Serials />} />
          <Route path="/films/:slug" element={<FilmDetail />} />
          <Route path="/serials/:slug" element={<SerialDetail />} />
        </Routes>
      </Layout>
    </Router>
  )
}
