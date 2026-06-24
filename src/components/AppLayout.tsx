import { NavLink, Outlet } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'
import { getScoreSummary } from '../lib/practice'
import { useLanguage } from '../context/LanguageContext'
import { useT } from '../lib/i18n'

export function AppLayout() {
  const practice = usePractice()
  const { total } = getScoreSummary(practice.session)
  const { language, toggleLanguage } = useLanguage()
  const t = useT()

  return (
    <div className="app-shell">
      {/* Ambient decorations */}
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />

      {/* Top bar */}
      <header className="topbar">
        <NavLink to="/" className="brand-block">
          <span className="brand-mark">MB</span>
          <div className="brand-copy">
            <strong>{t('brand', 'title')}</strong>
            <span className="eyebrow">{t('brand', 'subtitle')}</span>
          </div>
        </NavLink>

        <nav className="topnav">
          <NavLink to="/" className="nav-link" end>{t('nav', 'home')}</NavLink>
          <NavLink to="/categories" className="nav-link">{t('nav', 'categories')}</NavLink>
          <NavLink to="/practice" className="nav-link">{t('nav', 'practice')}</NavLink>
          <NavLink to="/mistakes" className="nav-link">{t('nav', 'mistakes')}</NavLink>
          <NavLink to="/review" className="nav-link">{t('nav', 'review')}</NavLink>
          <NavLink to="/vocabulary" className="nav-link">{t('nav', 'vocabulary')}</NavLink>
          <NavLink to="/results" className="nav-link">{t('nav', 'results')}</NavLink>
          <NavLink to="/about" className="nav-link">{t('nav', 'about')}</NavLink>
        </nav>

        <div className="status-group">
          <button className="lang-toggle" onClick={toggleLanguage} type="button" title={language === 'en' ? '切换到中文' : 'Switch to English'}>
            <span className={language === 'en' ? 'lang-active' : 'lang-inactive'}>EN</span>
            <span className="lang-sep">/</span>
            <span className={language === 'zh' ? 'lang-active' : 'lang-inactive'}>中</span>
          </button>
          <span className="status-pill">
            {t('status', 'answered')} <strong>{total}</strong> {t('status', 'questions')}
          </span>
          <span className="status-pill">
            {t('status', 'mistakes')} <strong>{practice.mistakeRecords.length}</strong>
          </span>
          <span className="status-pill">
            {t('status', 'vocab')} <strong>{practice.vocabularyRecords.length}</strong>
          </span>
        </div>
      </header>

      {/* Page content */}
      <main className="page-shell">
        <Outlet />
      </main>
    </div>
  )
}
