import { NavLink, Outlet } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'
import { getScoreSummary } from '../lib/practice'

export function AppLayout() {
  const practice = usePractice()
  const { total } = getScoreSummary(practice.session)

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
            <strong>分子生物学习题库</strong>
            <span className="eyebrow">Molecular Biology · ZJU</span>
          </div>
        </NavLink>

        <nav className="topnav">
          <NavLink to="/" className="nav-link" end>
            首页
          </NavLink>
          <NavLink to="/categories" className="nav-link">
            题型选择
          </NavLink>
          <NavLink to="/practice" className="nav-link">
            练习
          </NavLink>
          <NavLink to="/mistakes" className="nav-link">
            错题本
          </NavLink>
          <NavLink to="/review" className="nav-link">
            复习
          </NavLink>
          <NavLink to="/vocabulary" className="nav-link">
            生词本
          </NavLink>
          <NavLink to="/results" className="nav-link">
            结果
          </NavLink>
          <NavLink to="/about" className="nav-link">
            关于
          </NavLink>
        </nav>

        <div className="status-group">
          <span className="status-pill">
            已答 <strong>{total}</strong> 题
          </span>
          <span className="status-pill">
            错题 <strong>{practice.mistakeRecords.length}</strong>
          </span>
          <span className="status-pill">
            生词 <strong>{practice.vocabularyRecords.length}</strong>
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
