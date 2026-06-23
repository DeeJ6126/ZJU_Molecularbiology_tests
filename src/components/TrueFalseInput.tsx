import type { TrueFalseQuestion } from '../types'
import type { PracticeAnswer, AnswerSelection } from '../types'

interface TrueFalseInputProps {
  question: TrueFalseQuestion
  existingAnswer: PracticeAnswer | undefined
  onAnswer: (questionId: string, selectedKey: AnswerSelection) => void
}

export function TrueFalseInput({
  question,
  existingAnswer,
  onAnswer,
}: TrueFalseInputProps) {
  const answered = Boolean(existingAnswer)
  const isCorrect = existingAnswer?.isCorrect ?? false
  const userChoice = existingAnswer?.selectedKey

  function handleSelect(choice: AnswerSelection) {
    if (answered) return
    onAnswer(question.id, choice)
  }

  function getButtonClass(buttonKey: string) {
    if (!answered) return 'option-button'

    const isThisCorrect = (buttonKey === 'A') === question.answerIsTrue
    const isThisSelected = userChoice === buttonKey

    if (isThisCorrect) return 'option-button is-correct'
    if (isThisSelected && !isCorrect) return 'option-button is-incorrect'
    return 'option-button is-muted'
  }

  return (
    <div className="question-panel">
      <p className="question-text">{question.prompt}</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
        <button
          className={getButtonClass('A')}
          onClick={() => handleSelect('A')}
          disabled={answered}
          style={{ justifyContent: 'center', textAlign: 'center' }}
        >
          <strong>✓ 正确</strong>
        </button>

        <button
          className={getButtonClass('B')}
          onClick={() => handleSelect('B')}
          disabled={answered}
          style={{ justifyContent: 'center', textAlign: 'center' }}
        >
          <strong>✗ 错误</strong>
        </button>
      </div>

      {answered && (
        <div className={`answer-banner ${isCorrect ? 'is-visible' : ''}`}>
          {isCorrect ? (
            <strong style={{ color: 'var(--correct)' }}>✓ 回答正确！</strong>
          ) : (
            <strong style={{ color: 'var(--incorrect)' }}>
              ✗ 回答错误，正确答案是：{question.answerIsTrue ? '正确' : '错误'}
            </strong>
          )}
          {question.explanation && (
            <div className="explanation-panel" style={{ marginTop: 12 }}>
              <strong>解析</strong>
              <p>{question.explanation}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
