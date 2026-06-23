import { useState } from 'react'
import type { EssayQuestion } from '../types'
import type { PracticeAnswer } from '../types'

interface EssayInputProps {
  question: EssayQuestion
  existingAnswer: PracticeAnswer | undefined
  onSelfJudge: (questionId: string, isCorrect: boolean) => void
}

export function EssayInput({
  question,
  existingAnswer,
  onSelfJudge,
}: EssayInputProps) {
  const [revealed, setRevealed] = useState(false)
  const [draft, setDraft] = useState('')
  const judged = Boolean(existingAnswer)
  const selfJudgedCorrect = existingAnswer?.selfJudgedCorrect

  function handleReveal() {
    setRevealed(true)
  }

  function handleSelfJudge(isCorrect: boolean) {
    if (judged) return
    onSelfJudge(question.id, isCorrect)
  }

  return (
    <div className="question-panel">
      <p className="question-text">{question.prompt}</p>
      <p className="panel-note" style={{ marginTop: 0 }}>
        论述题 — 请在草稿区写下你的思路，然后查看参考答案并自主判断
      </p>

      {!judged && (
        <textarea
          className="option-button"
          style={{
            width: '100%',
            minHeight: 180,
            resize: 'vertical',
            fontFamily: 'inherit',
          }}
          placeholder="在此输入你的分析论述（可选）..."
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
        />
      )}

      {!revealed && !judged && (
        <button className="primary-button" onClick={handleReveal} style={{ width: '100%' }}>
          显示参考答案
        </button>
      )}

      {revealed && (
        <div className="answer-banner is-visible">
          <strong>参考答案</strong>
          <div
            style={{ whiteSpace: 'pre-wrap', lineHeight: 1.7 }}
          >
            {question.referenceAnswer}
          </div>
        </div>
      )}

      {revealed && !judged && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
          <button
            className="option-button"
            style={{
              justifyContent: 'center',
              textAlign: 'center',
              borderColor: 'rgba(31,122,86,0.4)',
              background: 'var(--correct-soft)',
            }}
            onClick={() => handleSelfJudge(true)}
          >
            <strong style={{ color: 'var(--correct)' }}>我基本答对了</strong>
          </button>
          <button
            className="option-button"
            style={{
              justifyContent: 'center',
              textAlign: 'center',
              borderColor: 'rgba(182,86,66,0.4)',
              background: 'var(--incorrect-soft)',
            }}
            onClick={() => handleSelfJudge(false)}
          >
            <strong style={{ color: 'var(--incorrect)' }}>我答错了</strong>
          </button>
        </div>
      )}

      {judged && (
        <div className={`answer-banner ${selfJudgedCorrect ? 'is-visible' : ''}`}>
          {selfJudgedCorrect ? (
            <strong style={{ color: 'var(--correct)' }}>✓ 你判断自己回答正确</strong>
          ) : (
            <strong style={{ color: 'var(--incorrect)' }}>
              ✗ 你判断自己回答错误，已加入错题本
            </strong>
          )}
          <div className="explanation-panel" style={{ marginTop: 12 }}>
            <strong>参考答案</strong>
            <p style={{ whiteSpace: 'pre-wrap' }}>{question.referenceAnswer}</p>
          </div>
        </div>
      )}
    </div>
  )
}
