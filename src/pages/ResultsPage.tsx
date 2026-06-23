import { Link, Navigate } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'
import { getScoreSummary } from '../lib/practice'

export function ResultsPage() {
  const practice = usePractice()
  const { session, questionBank } = practice

  if (!session || !session.answers.length) {
    return <Navigate replace to="/categories" />
  }

  const {
    total,
    answered,
    correct,
    selfJudgedCorrect,
    selfJudgedIncorrect,
    unanswered,
    accuracy,
  } = getScoreSummary(session)

  // Group answers by question type
  const typeStats: Record<string, { total: number; correct: number }> = {}
  for (const qid of session.questionOrder) {
    const q = questionBank.questions.find((qq) => qq.id === qid)
    if (!q) continue
    if (!typeStats[q.type]) {
      typeStats[q.type] = { total: 0, correct: 0 }
    }
    typeStats[q.type].total += 1
    const answer = session.answers.find((a) => a.questionId === qid)
    if (answer?.isCorrect) {
      typeStats[q.type].correct += 1
    }
  }

  const typeLabels: Record<string, string> = {
    translation: '名词互译',
    'true-false': '判断',
    'multiple-choice': '选择',
    'short-answer': '简答',
    essay: '论述',
  }

  // Categories included
  const selectedCats = questionBank.categories.filter((c) =>
    session.selectedCategoryIds.includes(c.id),
  )

  return (
    <div className="page-stack">
      {/* Spotlight */}
      <section className="panel result-spotlight">
        <h1 style={{ fontSize: 'clamp(3rem, 5vw, 5rem)' }}>{accuracy}%</h1>
        <p className="panel-note">正确率</p>
        <p>
          {answered} / {total} 已答 · {correct} 正确
          {selfJudgedCorrect > 0 && ` · ${selfJudgedCorrect} 自主判对`}
          {selfJudgedIncorrect > 0 && ` · ${selfJudgedIncorrect} 自主判错`}
        </p>
      </section>

      {/* Stats cards */}
      <section className="result-grid">
        <div className="panel result-card">
          <strong>{total}</strong>
          <span>总题数</span>
        </div>
        <div className="panel result-card">
          <strong>{answered}</strong>
          <span>已作答</span>
        </div>
        <div className="panel result-card">
          <strong>{correct}</strong>
          <span>正确</span>
        </div>
        <div className="panel result-card">
          <strong>{unanswered}</strong>
          <span>未作答</span>
        </div>
      </section>

      {/* Per-type breakdown */}
      {Object.keys(typeStats).length > 0 && (
        <section className="panel compact-panel">
          <h2 style={{ marginBottom: 14 }}>按题型统计</h2>
          <div className="chapter-grid">
            {Object.entries(typeStats).map(([type, stats]) => (
              <div key={type} className="chapter-card" style={{ cursor: 'default' }}>
                <div className="chapter-card-top">
                  <span className="chapter-chip">{typeLabels[type] || type}</span>
                  <span className="chapter-count">
                    {stats.total > 0
                      ? `${Math.round((stats.correct / stats.total) * 100)}%`
                      : '—'}
                  </span>
                </div>
                <p style={{ color: 'var(--ink-soft)' }}>
                  {stats.correct} / {stats.total} 正确
                </p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Selected categories */}
      {selectedCats.length > 0 && (
        <section className="panel compact-panel">
          <h2 style={{ marginBottom: 14 }}>本次练习范围</h2>
          <div className="chapter-pill-row">
            {selectedCats.map((cat) => (
              <span key={cat.id} className="chapter-pill">
                {cat.parentTitle && `${cat.parentTitle} · `}
                {cat.title}
              </span>
            ))}
          </div>
        </section>
      )}

      {/* Actions */}
      <section className="cta-row">
        <button
          className="primary-button"
          onClick={() => practice.restartPractice()}
        >
          再做一次
        </button>
        <Link to="/categories" className="secondary-button">
          返回题型选择
        </Link>
        {practice.mistakeRecords.length > 0 && (
          <Link to="/mistakes" className="ghost-button">
            查看错题本
          </Link>
        )}
      </section>
    </div>
  )
}
