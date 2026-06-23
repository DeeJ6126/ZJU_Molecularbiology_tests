import type { MultipleChoiceQuestion } from '../types'
import type { PracticeAnswer, AnswerSelection } from '../types'

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
  const answered = Boolean(existingAnswer)
  const isCorrect = existingAnswer?.isCorrect ?? false
  const selectedKey = existingAnswer?.selectedKey
  const correctKey = question.answerKey

  function handleSelect(key: AnswerSelection) {
    if (answered) return
    onAnswer(question.id, key)
  }

  // If distractors not yet generated, show placeholder
  if (!question.distractorsGenerated || !question.options.length) {
    return (
      <div className="question-panel">
        <p className="question-text">{question.prompt}</p>
        <div className="inset-panel" style={{ textAlign: 'center', padding: 32 }}>
          <p className="panel-note">
            该题目的选项尚未生成。答案：{question.answerText || question.answerKey || '未知'}
          </p>
          {question.explanation && (
            <div className="explanation-panel" style={{ marginTop: 16 }}>
              <strong>解析</strong>
              <p>{question.explanation}</p>
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="question-panel">
      <p className="question-text">{question.prompt}</p>

      <div className="option-list">
        {question.options.map((option) => {
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
              <span>{option.text}</span>
            </button>
          )
        })}
      </div>

      {answered && (
        <div className={`answer-banner ${isCorrect ? 'is-visible' : ''}`}>
          {isCorrect ? (
            <strong style={{ color: 'var(--correct)' }}>✓ 回答正确！</strong>
          ) : (
            <strong style={{ color: 'var(--incorrect)' }}>
              ✗ 回答错误，正确答案是：{correctKey}
            </strong>
          )}
          {question.explanation && (
            <div className="explanation-panel">
              <strong>解析</strong>
              <p>{question.explanation}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
