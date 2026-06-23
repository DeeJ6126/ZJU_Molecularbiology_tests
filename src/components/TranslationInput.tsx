import { useState } from 'react'
import type { TranslationQuestion, PracticeAnswer } from '../types'

interface TranslationInputProps {
  question: TranslationQuestion
  existingAnswer: PracticeAnswer | undefined
  onAnswer: (questionId: string, textAnswer: string) => void
}

export function TranslationInput({
  question,
  existingAnswer,
  onAnswer,
}: TranslationInputProps) {
  const [input, setInput] = useState(existingAnswer?.textAnswer ?? '')
  const answered = Boolean(existingAnswer)
  const isCorrect = existingAnswer?.isCorrect ?? false

  function handleSubmit() {
    if (answered || !input.trim()) return
    onAnswer(question.id, input.trim())
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLInputElement>) {
    if (event.key === 'Enter') {
      event.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="question-panel">
      {/* Prompt */}
      <p className="question-text">{question.prompt}</p>
      <p className="panel-note" style={{ marginTop: 0 }}>
        请输入中文翻译
      </p>

      {/* Input */}
      <input
        type="text"
        className="option-button"
        style={{ width: '100%', padding: '16px 18px' }}
        placeholder="输入你的翻译..."
        value={input}
        onChange={(event) => setInput(event.target.value)}
        onKeyDown={handleKeyDown}
        disabled={answered}
      />

      {/* Submit button */}
      {!answered && (
        <button
          className="primary-button"
          onClick={handleSubmit}
          disabled={!input.trim()}
          style={{ width: '100%' }}
        >
          提交
        </button>
      )}

      {/* Feedback banner */}
      {answered && (
        <div className={`answer-banner ${isCorrect ? 'is-visible' : ''}`}>
          {isCorrect ? (
            <strong style={{ color: 'var(--correct)' }}>✓ 回答正确！</strong>
          ) : (
            <>
              <strong style={{ color: 'var(--incorrect)' }}>✗ 回答错误</strong>
              <p>
                正确答案：
                {question.chineseMeaning || question.answerTerm}
                {question.answerFullTerm && (
                  <span style={{ color: 'var(--ink-soft)', marginLeft: 8 }}>
                    ({question.answerFullTerm})
                  </span>
                )}
              </p>
            </>
          )}
          {!isCorrect && question.acceptableAnswers.length > 1 && (
            <p style={{ color: 'var(--ink-soft)', fontSize: '0.9rem', marginTop: 4 }}>
              可接受答案：{question.acceptableAnswers.join(' / ')}
            </p>
          )}
          {!isCorrect && existingAnswer?.textAnswer && (
            <p style={{ color: 'var(--ink-soft)', marginTop: 4 }}>
              你的回答：{existingAnswer.textAnswer}
            </p>
          )}
        </div>
      )}
    </div>
  )
}
