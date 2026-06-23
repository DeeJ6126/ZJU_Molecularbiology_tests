import { useNavigate } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'

const TYPE_LABELS: Record<string, string> = {
  translation: '名词互译',
  'true-false': '判断',
  'multiple-choice': '选择',
  'short-answer': '简答',
  essay: '论述',
}

export function MistakesPage() {
  const navigate = useNavigate()
  const practice = usePractice()
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
            <h2>错题本</h2>
            <p className="scope-note">
              共 <strong>{mistakeRecords.length}</strong> 道错题。
              {mistakeRecords.length > 0 && '点击"开始错题练习"进行针对性复习。'}
            </p>
          </div>
          <div className="toolbar-actions">
            {mistakeRecords.length > 0 && (
              <>
                <button className="primary-button" onClick={handleStartDrill}>
                  开始错题练习
                </button>
                <button className="ghost-button" onClick={clearMistakes}>
                  清空全部
                </button>
              </>
            )}
          </div>
        </div>
      </section>

      {!mistakeRecords.length ? (
        <section className="panel empty-state">
          <h2>错题本为空</h2>
          <p>完成练习后，答错的题目会自动加入错题本。简答题选择"我答错了"也会加入。</p>
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
                    {TYPE_LABELS[record.questionType] || record.questionType}
                  </span>
                  <span
                    className="chapter-count"
                    style={{ background: 'var(--incorrect-soft)', color: 'var(--incorrect)' }}
                  >
                    错 {record.wrongCount} 次
                  </span>
                </div>

                <p className="mistake-question" style={{ fontSize: '1.1rem' }}>
                  #{question.number} {question.prompt.slice(0, 150)}
                  {question.prompt.length > 150 ? '...' : ''}
                </p>

                <div className="mistake-answer-row">
                  {record.lastSelectedKey && (
                    <span className="mistake-answer-pill is-wrong">
                      你的答案：{record.lastSelectedKey}
                    </span>
                  )}
                  {record.lastTextAnswer && (
                    <span className="mistake-answer-pill is-wrong">
                      你的答案：{record.lastTextAnswer}
                    </span>
                  )}
                  <span className="mistake-answer-pill is-correct">
                    正确答案：{record.correctAnswerDisplay.slice(0, 80)}
                  </span>
                </div>

                <button
                  className="ghost-button"
                  onClick={() => removeMistake(record.questionId)}
                  style={{ marginTop: 8 }}
                >
                  从错题本移除
                </button>
              </section>
            )
          })}
        </div>
      )}
    </div>
  )
}
