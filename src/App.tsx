import { Navigate, Route, Routes } from 'react-router-dom'
import { useQuestionBank } from './hooks/useQuestionBank'
import { PracticeProvider } from './context/PracticeContext'
import { AppLayout } from './components/AppLayout'
import { IntroPage } from './pages/IntroPage'
import { CategorySelectionPage } from './pages/CategorySelectionPage'
import { PracticePage } from './pages/PracticePage'
import { ResultsPage } from './pages/ResultsPage'
import { MistakesPage } from './pages/MistakesPage'
import { ReviewPage } from './pages/ReviewPage'
import { VocabularyPage } from './pages/VocabularyPage'
import { AboutPage } from './pages/AboutPage'
import { useT } from './lib/i18n'
import './App.css'

export function App() {
  const { questionBank, loading, error, reload } = useQuestionBank()
  const t = useT()

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="status-panel">
          <h1>{t('app', 'loadingTitle')}</h1>
          <p>{t('app', 'loading')}</p>
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
          <h1>{t('app', 'errorTitle')}</h1>
          <p>{error}</p>
          <button className="primary-button" onClick={reload} style={{ marginTop: 16 }}>
            {t('app', 'reload')}
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
          <Route path="/review" element={<ReviewPage />} />
          <Route path="/vocabulary" element={<VocabularyPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="*" element={<Navigate replace to="/" />} />
        </Route>
      </Routes>
    </PracticeProvider>
  )
}
