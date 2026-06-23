import { Navigate, Route, Routes } from 'react-router-dom'
import { useQuestionBank } from './hooks/useQuestionBank'
import { PracticeProvider } from './context/PracticeContext'
import { AppLayout } from './components/AppLayout'
import { IntroPage } from './pages/IntroPage'
import { CategorySelectionPage } from './pages/CategorySelectionPage'
import { PracticePage } from './pages/PracticePage'
import { ResultsPage } from './pages/ResultsPage'
import { MistakesPage } from './pages/MistakesPage'
import { VocabularyPage } from './pages/VocabularyPage'
import { AboutPage } from './pages/AboutPage'
import './App.css'

export function App() {
  const { questionBank, loading, error, reload } = useQuestionBank()

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="status-panel">
          <h1>分子生物学习题库</h1>
          <p>正在加载题库…</p>
          <div className="progress-track" style={{ marginTop: 16 }}>
            <span className="progress-fill" style={{ width: '60%' }} />
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="loading-screen">
        <div className="status-panel">
          <h1>题库加载失败</h1>
          <p>{error}</p>
          <button className="primary-button" onClick={reload} style={{ marginTop: 16 }}>
            重新加载
          </button>
        </div>
      </div>
    )
  }

  if (!questionBank) {
    return null
  }

  return (
    <PracticeProvider questionBank={questionBank}>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<IntroPage />} />
          <Route path="/categories" element={<CategorySelectionPage />} />
          <Route path="/practice" element={<PracticePage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/mistakes" element={<MistakesPage />} />
          <Route path="/vocabulary" element={<VocabularyPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="*" element={<Navigate replace to="/" />} />
        </Route>
      </Routes>
    </PracticeProvider>
  )
}
