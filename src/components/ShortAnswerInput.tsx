import { useState } from 'react'
import type { ShortAnswerQuestion } from '../types'
import type { PracticeAnswer } from '../types'
import { useLanguage } from '../context/LanguageContext'
import { useT } from '../lib/i18n'

interface ShortAnswerInputProps {
  question: ShortAnswerQuestion
  existingAnswer: PracticeAnswer | undefined
  onSelfJudge: (questionId: string, isCorrect: boolean) => void
}

export function ShortAnswerInput({
  question,
  existingAnswer,
  onSelfJudge,
}: ShortAnswerInputProps) {
  const { language } = useLanguage()
  const t = useT()
  const [revealed, setRevealed] = useState(false)
  const [draft, setDraft] = useState('')
  const judged = Boolean(existingAnswer)
  const selfJudgedCorrect = existingAnswer?.selfJudgedCorrect

  const prompt = language === 'zh' ? (question.promptCn ?? question.prompt) : question.prompt

  function handleReveal() {
    setRevealed(true)
  }

  function handleSelfJudge(isCorrect: boolean) {
    if (judged) return
    onSelfJudge(question.id, isCorrect)
  }

  return (
    <div className="question-panel">
      <p className="question-text">{prompt}</p>

      {/* Textarea for user to draft their answer */}
      {!judged && (
        <textarea
          className="option-button"
          style={{
            width: '100%',
            minHeight: 120,
            resize: 'vertical',
            fontFamily: 'inherit',
          }}
          placeholder={t('sa', 'placeholder')}
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
        />
      )}

      {/* Reveal button */}
      {!revealed && !judged && (
        <button className="primary-button" onClick={handleReveal} style={{ width: '100%' }}>
          {t('sa', 'reveal')}
        </button>
      )}

      {/* Reference answer */}
      {revealed && (
        <div className="answer-banner is-visible">
          <strong>{t('sa', 'reference')}</strong>
          <div
            style={{ whiteSpace: 'pre-wrap', lineHeight: 1.7 }}
          >
            {question.referenceAnswer}
          </div>
        </div>
      )}

      {/* Self-judge buttons (after reveal, before judging) */}
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
            <strong style={{ color: 'var(--correct)' }}>{t('sa', 'gotIt')}</strong>
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
            <strong style={{ color: 'var(--incorrect)' }}>{t('sa', 'gotWrong')}</strong>
          </button>
        </div>
      )}

      {/* Post-judge state */}
      {judged && (
        <div className={`answer-banner ${selfJudgedCorrect ? 'is-visible' : ''}`}>
          {selfJudgedCorrect ? (
            <strong style={{ color: 'var(--correct)' }}>{t('sa', 'judgedCorrect')}</strong>
          ) : (
            <strong style={{ color: 'var(--incorrect)' }}>
              {t('sa', 'judgedWrong')}
            </strong>
          )}
          <div className="explanation-panel" style={{ marginTop: 12 }}>
            <strong>{t('sa', 'reference')}</strong>
            <p style={{ whiteSpace: 'pre-wrap' }}>{question.referenceAnswer}</p>
          </div>
        </div>
      )}
    </div>
  )
}
