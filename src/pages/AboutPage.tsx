import { useT } from '../lib/i18n'

export function AboutPage() {
  const t = useT()

  return (
    <div className="page-stack">
      <section className="panel hero-panel">
        <h1>{t('about', 'title')}</h1>
        <p className="lead" style={{ marginTop: 16 }}>
          {t('about', 'desc')}
        </p>
      </section>

      <section className="panel compact-panel">
        <h2 style={{ marginBottom: 16 }}>{t('about', 'contentTitle')}</h2>
        <div className="about-list" style={{ gap: 12 }}>
          <div className="about-row">
            <strong>{t('about', 'source')}</strong>
            <span>{t('about', 'sourceDesc')}</span>
          </div>
          <div className="about-row">
            <strong>{t('about', 'types')}</strong>
            <span>{t('about', 'typesDesc')}</span>
          </div>
          <div className="about-row">
            <strong>{t('about', 'abbreviation')}</strong>
            <span>{t('about', 'abbreviationDesc')}</span>
          </div>
          <div className="about-row">
            <strong>{t('about', 'selfJudge')}</strong>
            <span>{t('about', 'selfJudgeDesc')}</span>
          </div>
          <div className="about-row">
            <strong>{t('about', 'mistakes')}</strong>
            <span>{t('about', 'mistakesDesc')}</span>
          </div>
          <div className="about-row">
            <strong>{t('about', 'vocab')}</strong>
            <span>{t('about', 'vocabDesc')}</span>
          </div>
        </div>
      </section>

      <section className="panel compact-panel">
        <h2 style={{ marginBottom: 16 }}>{t('about', 'techTitle')}</h2>
        <p className="panel-note">
          {t('about', 'techDesc')}
        </p>
      </section>
    </div>
  )
}
