import { useCallback, useEffect, useState } from 'react'
import type { TranslationQuestion, PracticeAnswer } from '../types'

// Acronyms that sound natural when spoken as-is by TTS
const PRONOUNCEABLE_ACRONYMS = new Set(['DNA', 'RNA'])

interface TranslationInputProps {
  question: TranslationQuestion
  existingAnswer: PracticeAnswer | undefined
  onAnswer: (questionId: string, textAnswer: string) => void
  onNext?: () => void
  onPrev?: () => void
  onRemoveMistake?: (questionId: string) => void
}

export function TranslationInput({
  question,
  existingAnswer,
  onAnswer,
  onNext,
  onPrev,
  onRemoveMistake,
}: TranslationInputProps) {
  const [input, setInput] = useState(existingAnswer?.textAnswer ?? '')
  const [pending, setPending] = useState(false)
  const [removedFromMistakes, setRemovedFromMistakes] = useState(false)

  // Reset when question changes: clear input for new questions, restore for answered ones
  useEffect(() => {
    setInput(existingAnswer?.textAnswer ?? '')
    setPending(false)
    setRemovedFromMistakes(false)
  }, [question.id, existingAnswer?.textAnswer])

  const shouldWait = pending && !Boolean(existingAnswer)  // submitted but waiting for parent
  const answered = pending || Boolean(existingAnswer)
  const isCorrect = existingAnswer?.isCorrect ?? false

  const isZhToEn = question.direction === 'zh-to-en'

  // Pronunciation: speak the full term (not abbreviation) via Web Speech API
  const speak = useCallback(() => {
    if (!question || typeof speechSynthesis === 'undefined') return

    speechSynthesis.cancel()

    const abbr = question.answerFullTerm
    const full = question.answerTerm

    let textToSpeak: string
    if (abbr && PRONOUNCEABLE_ACRONYMS.has(abbr)) {
      // DNA, RNA sound fine as-is
      textToSpeak = abbr
    } else {
      // Always prefer the full term for pronunciation
      textToSpeak = full
    }

    const utterance = new SpeechSynthesisUtterance(textToSpeak)
    utterance.lang = 'en-US'
    utterance.rate = 0.85
    speechSynthesis.speak(utterance)
  }, [question])

  // Global keyboard shortcuts (arrow nav, space-to-next, shift-to-speak)
  useEffect(() => {
    const next = onNext
    const prev = onPrev

    function handleKeyDown(event: KeyboardEvent) {
      // Don't intercept when user is typing in an input/textarea
      if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) {
        return
      }

      switch (event.code) {
        case 'ArrowLeft':
          event.preventDefault()
          prev?.()
          break
        case 'ArrowRight':
          event.preventDefault()
          next?.()
          break
        case 'Space':
          // After answering, Space goes to next question
          if (Boolean(existingAnswer) && next) {
            event.preventDefault()
            next()
          }
          break
        case 'ShiftLeft':
        case 'ShiftRight':
          event.preventDefault()
          speak()
          break
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [Boolean(existingAnswer), onNext, onPrev, speak])

  function handleSubmit() {
    if (pending || Boolean(existingAnswer) || !input.trim()) return
    setPending(true)
    onAnswer(question.id, input.trim())
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLInputElement>) {
    if (event.key === 'Enter') {
      event.preventDefault()
      handleSubmit()
    }
  }

  function handleRemoveMistake() {
    if (!onRemoveMistake) return
    setRemovedFromMistakes(true)
    onRemoveMistake(question.id)
  }

  function buildAnswerDisplay(): string {
    if (isZhToEn) {
      const parts: string[] = [question.answerTerm]
      if (question.answerFullTerm && question.answerFullTerm !== question.answerTerm) {
        parts.push(`(${question.answerFullTerm})`)
      }
      return parts.join(' ')
    }
    return question.chineseMeaning || ''
  }

  function buildAcceptableDisplay(): string {
    const seen = new Set<string>()
    const parts: string[] = []
    if (isZhToEn) {
      if (question.answerTerm && !seen.has(question.answerTerm)) {
        parts.push(question.answerTerm)
        seen.add(question.answerTerm)
      }
      if (question.answerFullTerm && !seen.has(question.answerFullTerm)) {
        parts.push(question.answerFullTerm)
        seen.add(question.answerFullTerm)
      }
      if (question.answerTerm && question.answerFullTerm) {
        const combined = `${question.answerTerm} (${question.answerFullTerm})`
        if (!seen.has(combined)) parts.push(combined)
      }
    }
    return parts.join(' / ')
  }

  return (
    <div className="question-panel">
      <p className="question-text">{question.prompt}</p>
      <p className="panel-note" style={{ marginTop: 0 }}>
        {isZhToEn
          ? '请输入英文翻译（Enter 提交，← → 切题，Space 下一题，Shift 发音）'
          : '请输入中文翻译'}
      </p>

      <input
        type="text"
        className="option-button"
        style={{ width: '100%', padding: '16px 18px' }}
        placeholder={isZhToEn ? '输入英文翻译...' : '输入中文翻译...'}
        value={input}
        onChange={(event) => setInput(event.target.value)}
        onKeyDown={handleKeyDown}
        disabled={answered}
        autoFocus
      />

      {!shouldWait && !Boolean(existingAnswer) && (
        <button
          className="primary-button"
          onClick={handleSubmit}
          disabled={!input.trim()}
          style={{ width: '100%' }}
        >
          提交
        </button>
      )}

      {shouldWait && (
        <p style={{ color: 'var(--ink-soft)', textAlign: 'center', padding: 12 }}>
          提交中...
        </p>
      )}

      {/* Feedback after answering */}
      {Boolean(existingAnswer) && (
        <>
          <div className={`answer-banner ${isCorrect ? 'is-visible' : ''}`}>
            {isCorrect ? (
              <strong style={{ color: 'var(--correct)' }}>✓ 回答正确！</strong>
            ) : (
              <>
                <strong style={{ color: 'var(--incorrect)' }}>✗ 回答错误</strong>
                <p>正确答案：{buildAnswerDisplay()}</p>
              </>
            )}
            {!isCorrect && (
              <p style={{ color: 'var(--ink-soft)', fontSize: '0.9rem', marginTop: 4 }}>
                {isZhToEn
                  ? `可接受答案：${buildAcceptableDisplay()}`
                  : `可接受答案：${question.chineseMeaning || ''}`}
              </p>
            )}
            {!isCorrect && input && (
              <p style={{ color: 'var(--ink-soft)', marginTop: 4 }}>
                你的回答：{input}
              </p>
            )}
          </div>

          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginTop: 8 }}>
            {!isCorrect && !removedFromMistakes && onRemoveMistake && (
              <button className="ghost-button" onClick={handleRemoveMistake}>
                不放入错题本
              </button>
            )}
            {!isCorrect && removedFromMistakes && (
              <span style={{ color: 'var(--ink-soft)', fontSize: '0.9rem' }}>
                ✓ 已从错题本移除
              </span>
            )}
            {onNext && (
              <button className="secondary-button" onClick={onNext}>
                {isCorrect ? '下一题 →' : '下一题 (Space)'}
              </button>
            )}
          </div>
        </>
      )}
    </div>
  )
}
