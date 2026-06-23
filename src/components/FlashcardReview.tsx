import { useEffect, useState, useCallback } from 'react'
import type { TranslationQuestion } from '../types'
import { shuffleArray } from '../lib/practice'

interface FlashcardReviewProps {
  questions: TranslationQuestion[]
}

export function FlashcardReview({ questions }: FlashcardReviewProps) {
  const [shuffled] = useState(() => shuffleArray([...questions]))
  const [index, setIndex] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)

  const current = shuffled[index]
  const total = shuffled.length

  const goNext = useCallback(() => {
    setShowAnswer(false)
    setIndex((i) => (i + 1) % total)
  }, [total])

  const goPrev = useCallback(() => {
    setShowAnswer(false)
    setIndex((i) => (i - 1 + total) % total)
  }, [total])

  const toggleAnswer = useCallback(() => {
    setShowAnswer((v) => !v)
  }, [])

  const speak = useCallback(() => {
    if (!current || typeof speechSynthesis === 'undefined') return

    speechSynthesis.cancel()

    // For abbreviations, speak the full term if available
    const textToSpeak = current.answerFullTerm || current.answerTerm
    const utterance = new SpeechSynthesisUtterance(textToSpeak)
    utterance.lang = 'en-US'
    utterance.rate = 0.85
    speechSynthesis.speak(utterance)
  }, [current])

  // Keyboard shortcuts
  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      // Ignore if user is typing in an input
      if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) {
        return
      }

      switch (event.code) {
        case 'Enter':
          event.preventDefault()
          toggleAnswer()
          break
        case 'ArrowLeft':
          event.preventDefault()
          goPrev()
          break
        case 'ArrowRight':
          event.preventDefault()
          goNext()
          break
        case 'Space':
          event.preventDefault()
          speak()
          break
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [toggleAnswer, goPrev, goNext, speak])

  if (!current) {
    return (
      <section className="panel empty-state">
        <h2>暂无复习词汇</h2>
        <p>请先在题型选择页勾选翻译子分类。</p>
      </section>
    )
  }

  return (
    <div className="page-stack" style={{ alignItems: 'center', textAlign: 'center' }}>
      {/* Progress */}
      <div className="progress-track" style={{ width: '100%' }}>
        <span
          className="progress-fill"
          style={{ width: `${((index + 1) / total) * 100}%` }}
        />
      </div>

      <span className="status-pill" style={{ marginTop: 8 }}>
        {index + 1} / {total}
      </span>

      {/* Flash card */}
      <section
        className="panel hero-panel"
        style={{
          width: '100%',
          minHeight: 320,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 24,
          cursor: 'pointer',
        }}
        onClick={toggleAnswer}
      >
        {/* English term */}
        <h1
          style={{
            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            fontFamily: 'var(--font-body)',
            fontWeight: 600,
            letterSpacing: '-0.02em',
          }}
        >
          {current.answerTerm}
          {current.answerFullTerm && current.answerFullTerm !== current.answerTerm && (
            <span style={{ fontSize: '0.5em', color: 'var(--ink-soft)', display: 'block', marginTop: 8 }}>
              ({current.answerFullTerm})
            </span>
          )}
        </h1>

        {/* Chinese translation (toggled by Enter) */}
        {showAnswer && (
          <div
            className="answer-banner is-visible"
            style={{ fontSize: '1.3rem', marginTop: 8 }}
          >
            <strong>{current.chineseMeaning}</strong>
          </div>
        )}

        {!showAnswer && (
          <p className="panel-note" style={{ marginTop: 8 }}>
            按 Enter / 点击卡片 显示中文翻译
          </p>
        )}
      </section>

      {/* Controls */}
      <div className="practice-actions" style={{ justifyContent: 'center' }}>
        <button className="secondary-button" onClick={goPrev}>
          ← 上一个
        </button>
        <button className="primary-button" onClick={toggleAnswer}>
          {showAnswer ? '隐藏翻译' : '显示翻译 (Enter)'}
        </button>
        <button className="ghost-button" onClick={speak} title="按空格键发音">
          🔊 发音 (Space)
        </button>
        <button className="secondary-button" onClick={goNext}>
          下一个 →
        </button>
      </div>

      <p className="panel-note">
        键盘快捷键：← 上一个 | → 下一个 | Enter 显示/隐藏翻译 | Space 发音
      </p>
    </div>
  )
}
