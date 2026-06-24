import { Link } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'
import { getQuestionTypes } from '../lib/categoryScope'
import { useT } from '../lib/i18n'

export function IntroPage() {
  const practice = usePractice()
  const types = getQuestionTypes(practice.questionBank)
  const t = useT()

  return (
    <div className="page-stack">
      {/* Hero */}
      <section className="panel hero-panel hero-grid">
        <div className="hero-copy">
          <h1>{t('intro', 'title')}</h1>
          <p className="lead">
            {t('intro', 'subtitle')}
          </p>
          <div className="cta-row">
            <Link to="/categories" className="primary-button">
              {t('intro', 'startBtn')}
            </Link>
            {practice.session && (
              <Link to="/practice" className="secondary-button">
                {t('intro', 'resumeSession')}
              </Link>
            )}
            {practice.mistakeRecords.length > 0 && (
              <Link to="/mistakes" className="ghost-button">
                {t('intro', 'mistakesBtn').replace('{n}', String(practice.mistakeRecords.length))}
              </Link>
            )}
          </div>
        </div>

        <div className="metric-grid" style={{ flex: '0 0 320px' }}>
          <div className="metric-card">
            <strong>{practice.questionBank.totalQuestions}</strong>
            <span>{t('intro', 'totalQuestions')}</span>
          </div>
          <div className="metric-card">
            <strong>{types.length}</strong>
            <span>{t('intro', 'questionTypes')}</span>
          </div>
          <div className="metric-card">
            <strong>{practice.questionBank.categories.length}</strong>
            <span>{t('intro', 'subCategories')}</span>
          </div>
          <div className="metric-card">
            <strong>{practice.mistakeRecords.length}</strong>
            <span>{t('intro', 'pendingMistakes')}</span>
          </div>
        </div>
      </section>

      {/* Feature cards */}
      <section className="feature-grid">
        {types.map((type) => {
          const label = t('practice.typeLabels', type)
          const cats = practice.questionBank.categories.filter((c) => c.type === type)
          const count = cats.reduce((sum, c) => sum + c.questionCount, 0)
          return (
            <div key={type} className="panel feature-card">
              <h2>{label}</h2>
              <p>{t('intro', 'typeStats').replace('{count}', String(count)).replace('{cats}', String(cats.length))}</p>
              <p className="panel-note">
                {t('intro.typeDesc', type)}
              </p>
            </div>
          )
        })}
      </section>

      {/* Usage guide */}
      <section className="panel compact-panel">
        <h2 style={{ marginBottom: 16 }}>{t('intro', 'guideTitle')}</h2>
        <div className="timeline-grid">
          <div className="timeline-step">
            <strong>{t('intro', 'step1Title')}</strong>
            <p>{t('intro', 'step1Desc')}</p>
          </div>
          <div className="timeline-step">
            <strong>{t('intro', 'step2Title')}</strong>
            <p>{t('intro', 'step2Desc')}</p>
          </div>
          <div className="timeline-step">
            <strong>{t('intro', 'step3Title')}</strong>
            <p>{t('intro', 'step3Desc')}</p>
          </div>
          <div className="timeline-step">
            <strong>{t('intro', 'step4Title')}</strong>
            <p>{t('intro', 'step4Desc')}</p>
          </div>
        </div>
      </section>
    </div>
  )
}
