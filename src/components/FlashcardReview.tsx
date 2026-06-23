import { useEffect, useState, useCallback } from 'react'
import type { TranslationQuestion } from '../types'
import { shuffleArray } from '../lib/practice'

// Acronyms that sound natural when spoken as-is by TTS
const PRONOUNCEABLE_ACRONYMS = new Set(['DNA', 'RNA'])

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

    const abbr = current.answerFullTerm   // e.g. "tRNA", "ChIP"
    const full = current.answerTerm        // e.g. "transfer RNA", "Chromatin immunoprecipitation"

    let textToSpeak: string
    if (abbr && PRONOUNCEABLE_ACRONYMS.has(abbr)) {
      // DNA, RNA sound fine as-is
      textToSpeak = abbr
    } else if (abbr) {
      // mRNA, tRNA, ChIP, FRET, etc. → use the full term
      textToSpeak = full
    } else {
      // No abbreviation at all → speak the term directly
      textToSpeak = full
    }

    const utterance = new SpeechSynthesisUtterance(textToSpeak)
    utterance.lang = 'en-US'
    utterance.rate = 0.85
    speechSynthesis.speak(utterance)
  }, [current])

  // Keyboard shortcuts
  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
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

  function buildEnglishDisplay(): string {
    const parts: string[] = [current.answerTerm]
    if (current.answerFullTerm && current.answerFullTerm !== current.answerTerm) {
      parts.push(`(${current.answerFullTerm})`)
    }
    return parts.join(' ')
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

      {/* Flash card — shows Chinese, reveals English */}
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
        {/* Chinese prompt */}
        <h1
          style={{
            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            fontFamily: 'var(--font-body)',
            fontWeight: 600,
            letterSpacing: '-0.02em',
          }}
        >
          {current.prompt}
        </h1>

        {/* English translation (toggled by Enter) */}
        {showAnswer && (
          <div
            className="answer-banner is-visible"
            style={{ fontSize: '1.3rem', marginTop: 8 }}
          >
            <strong>{buildEnglishDisplay()}</strong>
          </div>
        )}

        {!showAnswer && (
          <p className="panel-note" style={{ marginTop: 8 }}>
            按 Enter / 点击卡片 显示英文翻译
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
