import { useNavigate } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'
import { useT } from '../lib/i18n'

export function MistakesPage() {
  const navigate = useNavigate()
  const practice = usePractice()
  const t = useT()
  const { questionBank, mistakeRecords, beginMistakePractice, removeMistake, clearMistakes } =
    practice

  function handleStartDrill() {
    beginMistakePractice()
    navigate('/practice')
  }

  return (
    <div className="page-stack">
      <section className="panel compact-panel">
        <div className="section-heading">
          <div>
            <h2>{t('mistakes', 'title')}</h2>
            <p className="scope-note">
              {t('mistakes', 'count').replace('{n}', String(mistakeRecords.length))}
              {mistakeRecords.length > 0 && ' ' + t('mistakes', 'hint')}
            </p>
          </div>
          <div className="toolbar-actions">
            {mistakeRecords.length > 0 && (
              <>
                <button className="primary-button" onClick={handleStartDrill}>
                  {t('mistakes', 'startDrillShort')}
                </button>
                <button className="ghost-button" onClick={clearMistakes}>
                  {t('mistakes', 'clearAll')}
                </button>
              </>
            )}
          </div>
        </div>
      </section>

      {!mistakeRecords.length ? (
        <section className="panel empty-state">
          <h2>{t('mistakes', 'emptyTitle')}</h2>
          <p>{t('mistakes', 'emptyDesc')}</p>
        </section>
      ) : (
        <div className="mistake-grid">
          {mistakeRecords.map((record) => {
            const question = questionBank.questions.find(
              (q) => q.id === record.questionId,
            )
            if (!question) return null

            return (
              <section key={record.questionId} className="panel mistake-card">
                <div className="mistake-card-top">
                  <span className="chapter-chip">
                    {t('mistakes.typeLabels', record.questionType)}
                  </span>
                  <span
                    className="chapter-count"
                    style={{ background: 'var(--incorrect-soft)', color: 'var(--incorrect)' }}
                  >
                    {t('mistakes', 'wrongCount').replace('{n}', String(record.wrongCount))}
                  </span>
                </div>

                <p className="mistake-question" style={{ fontSize: '1.1rem' }}>
                  #{question.number} {question.prompt.slice(0, 150)}
                  {question.prompt.length > 150 ? '...' : ''}
                </p>

                <div className="mistake-answer-row">
                  {record.lastSelectedKey && (
                    <span className="mistake-answer-pill is-wrong">
                      {t('mistakes', 'yourAnswer')}{record.lastSelectedKey}
                    </span>
                  )}
                  {record.lastTextAnswer && (
                    <span className="mistake-answer-pill is-wrong">
                      {t('mistakes', 'yourAnswer')}{record.lastTextAnswer}
                    </span>
                  )}
                  <span className="mistake-answer-pill is-correct">
                    {t('mistakes', 'correctAnswer')}{record.correctAnswerDisplay.slice(0, 80)}
                  </span>
                </div>

                <button
                  className="ghost-button"
                  onClick={() => removeMistake(record.questionId)}
                  style={{ marginTop: 8 }}
                >
                  {t('mistakes', 'removeFromMistakes')}
                </button>
              </section>
            )
          })}
        </div>
      )}
    </div>
  )
}
