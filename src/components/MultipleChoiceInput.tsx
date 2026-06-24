import type { MultipleChoiceQuestion } from '../types'
import type { PracticeAnswer, AnswerSelection } from '../types'
import { useLanguage } from '../context/LanguageContext'
import { useT } from '../lib/i18n'

interface MultipleChoiceInputProps {
  question: MultipleChoiceQuestion
  existingAnswer: PracticeAnswer | undefined
  onAnswer: (questionId: string, selectedKey: AnswerSelection) => void
}

export function MultipleChoiceInput({
  question,
  existingAnswer,
  onAnswer,
}: MultipleChoiceInputProps) {
  const { language } = useLanguage()
  const t = useT()
  const answered = Boolean(existingAnswer)
  const isCorrect = existingAnswer?.isCorrect ?? false
  const selectedKey = existingAnswer?.selectedKey
  const correctKey = question.answerKey

  const prompt = language === 'zh' ? (question.promptCn ?? question.prompt) : question.prompt
  const explanation = language === 'zh' ? (question.explanationCn ?? question.explanation) : question.explanation

  function handleSelect(key: AnswerSelection) {
    if (answered) return
    onAnswer(question.id, key)
  }

  // If distractors not yet generated, show placeholder
  if (!question.distractorsGenerated || !question.options.length) {
    return (
      <div className="question-panel">
        <p className="question-text">{prompt}</p>
        <div className="inset-panel" style={{ textAlign: 'center', padding: 32 }}>
          <p className="panel-note">
            {t('mc', 'noOptions')}{question.answerText || question.answerKey || '未知'}
          </p>
          {explanation && (
            <div className="explanation-panel" style={{ marginTop: 16 }}>
              <strong>{t('mc', 'explanation')}</strong>
              <p>{explanation}</p>
            </div>
          )}
        </div>
      </div>
    )
  }

  const correctOption = question.options.find((o) => o.key === correctKey)

  return (
    <div className="question-panel">
      <p className="question-text">{prompt}</p>

      <div className="option-list">
        {question.options.map((option) => {
          const optionText = language === 'zh' ? (option.textCn ?? option.text) : option.text
          let className = 'option-button'
          if (answered) {
            if (option.key === correctKey) {
              className += ' is-correct'
            } else if (option.key === selectedKey && !isCorrect) {
              className += ' is-incorrect'
            } else {
              className += ' is-muted'
            }
          }

          return (
            <button
              key={option.key}
              className={className}
              onClick={() => handleSelect(option.key)}
              disabled={answered}
              type="button"
            >
              <span className="option-key">{option.key}</span>
              <span>{optionText}</span>
            </button>
          )
        })}
      </div>

      {answered && (
        <div className={`answer-banner ${isCorrect ? 'is-visible' : ''}`}>
          {isCorrect ? (
            <strong style={{ color: 'var(--correct)' }}>{t('mc', 'correct')}</strong>
          ) : (
            <strong style={{ color: 'var(--incorrect)' }}>
              {t('mc', 'wrong')}
              {correctOption
                ? `${correctKey}. ${language === 'zh' ? (correctOption.textCn ?? correctOption.text) : correctOption.text}`
                : correctKey}
            </strong>
          )}
          {explanation && (
            <div className="explanation-panel">
              <strong>{t('mc', 'explanation')}</strong>
              <p>{explanation}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
