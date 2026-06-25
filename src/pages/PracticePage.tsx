import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'
import { findAnswer } from '../lib/practice'
import { TranslationInput } from '../components/TranslationInput'
import { TrueFalseInput } from '../components/TrueFalseInput'
import { MultipleChoiceInput } from '../components/MultipleChoiceInput'
import { ShortAnswerInput } from '../components/ShortAnswerInput'
import { EssayInput } from '../components/EssayInput'
import { VocabularyPicker } from '../components/VocabularyPicker'
import { createVocabularyRecord } from '../lib/vocabulary'
import { useT } from '../lib/i18n'
import type { AnswerSelection, VocabularySourceType } from '../types'

export function PracticePage() {
  const navigate = useNavigate()
  const practice = usePractice()
  const { questionBank, session, vocabularyRecords, addVocabularyRecord } =
    practice
  const t = useT()

  const currentSession = session!
  const [vocabPickEnabled, setVocabPickEnabled] = useState(false)

  // Redirect if no session
  if (!currentSession || !currentSession.questionOrder.length) {
    return <Navigate replace to="/categories" />
  }

  const currentQuestion = questionBank.questions.find(
    (q) => q.id === currentSession.questionOrder[currentSession.currentIndex],
  )

  if (!currentQuestion) {
    return (
      <div className="page-stack">
        <section className="panel empty-state">
          <p>{t('practice', 'notFound')}</p>
          <button
            className="primary-button"
            onClick={() => {
              practice.clearSession()
              navigate('/categories')
            }}
          >
            {t('practice', 'back')}
          </button>
        </section>
      </div>
    )
  }

  const existingAnswer = findAnswer(currentSession, currentQuestion.id)
  const isMistakeMode = currentSession.mode === 'mistakes'
  const hasMistake = practice.hasMistake(currentQuestion.id)
  const progress = ((currentSession.currentIndex + 1) / currentSession.questionOrder.length) * 100

  const isLastQuestion = currentSession.currentIndex >= currentSession.questionOrder.length - 1

  function handleNext() {
    if (isLastQuestion) {
      navigate('/results')
    } else {
      practice.goToIndex(currentSession.currentIndex + 1)
    }
  }

  function handlePrev() {
    practice.goToIndex(currentSession.currentIndex - 1)
  }

  function handleRestart() {
    practice.restartPractice()
  }

  function handleMistakeRemove() {
    practice.removeMistake(currentQuestion!.id)
  }

  function handleMistakeKeep() {
    const answer = findAnswer(currentSession, currentQuestion!.id)
    practice.keepMistake(
      currentQuestion!.id,
      answer?.selectedKey ?? 'UNKNOWN',
      answer?.textAnswer,
    )
  }

  function handleVocabPick(term: string) {
    if (!currentQuestion) return

    const sourceType: VocabularySourceType = 'practice'
    const existing = vocabularyRecords.find(
      (r) =>
        r.normalizedTerm === term.toLowerCase().trim() &&
        r.questionId === currentQuestion.id,
    )
    if (existing) return

    addVocabularyRecord(
      createVocabularyRecord({
        term,
        contextText: currentQuestion.prompt,
        sourceType,
        questionId: currentQuestion.id,
        questionNumber: currentQuestion.number,
        chapterId: undefined,
        chapterTitle: currentQuestion.categoryTitle,
      }),
    )
  }

  // Question type label
  const typeLabels: Record<string, string> = {
    translation: t('practice.typeLabels', 'translation'),
    'true-false': t('practice.typeLabels', 'true-false'),
    'multiple-choice': t('practice.typeLabels', 'multiple-choice'),
    'short-answer': t('practice.typeLabels', 'short-answer'),
    essay: t('practice.typeLabels', 'essay'),
  }

  return (
    <div className="page-stack">
      {/* Progress bar */}
      <div className="progress-track">
        <span className="progress-fill" style={{ width: `${progress}%` }} />
      </div>

      {/* Question meta */}
      <div className="question-meta">
        <span className="status-pill">
          {typeLabels[currentQuestion.type] || currentQuestion.type}
        </span>
        <span className="status-pill">
          {currentQuestion.categoryTitle}
        </span>
        <span className="status-pill">
          {t('practice', 'questionN')
            .replace('{n}', String(currentSession.currentIndex + 1))
            .replace('{m}', String(currentSession.questionOrder.length))}
        </span>
        {isMistakeMode && (
          <span className="status-pill" style={{ background: 'var(--coral-soft)', color: '#8c4d29' }}>
            {t('practice', 'mistakeMode')}
          </span>
        )}
        {currentQuestion.examSources && currentQuestion.examSources.length > 0 && (
          currentQuestion.examSources.map((src: string) => (
            <span key={src} className="status-pill" style={{ background: 'var(--teal-soft)', color: 'var(--teal-deep)', fontSize: '0.78rem' }}>
              {src}
            </span>
          ))
        )}
      </div>

      {/* Question-type-specific input */}
      <section className="panel">
        {currentQuestion.type === 'translation' && (
          <TranslationInput
            key={currentQuestion.id}
            question={currentQuestion}
            existingAnswer={existingAnswer}
            onAnswer={(qid, text) => practice.recordTextAnswer(qid, text)}
            onNext={handleNext}
            onPrev={handlePrev}
            onRemoveMistake={(qid) => practice.removeMistake(qid)}
          />
        )}

        {currentQuestion.type === 'true-false' && (
          <TrueFalseInput
            question={currentQuestion}
            existingAnswer={existingAnswer}
            onAnswer={(qid, key) => practice.recordAnswer(qid, key as AnswerSelection)}
          />
        )}

        {currentQuestion.type === 'multiple-choice' && (
          <MultipleChoiceInput
            question={currentQuestion}
            existingAnswer={existingAnswer}
            onAnswer={(qid, key) => practice.recordAnswer(qid, key as AnswerSelection)}
          />
        )}

        {currentQuestion.type === 'short-answer' && (
          <ShortAnswerInput
            question={currentQuestion}
            existingAnswer={existingAnswer}
            onSelfJudge={(qid, isCorrect) => practice.recordSelfJudge(qid, isCorrect)}
          />
        )}

        {currentQuestion.type === 'essay' && (
          <EssayInput
            question={currentQuestion}
            existingAnswer={existingAnswer}
            onSelfJudge={(qid, isCorrect) => practice.recordSelfJudge(qid, isCorrect)}
          />
        )}
      </section>

      {/* Mistake-mode actions */}
      {isMistakeMode && existingAnswer && (
        <section className="panel compact-panel">
          <div style={{ display: 'flex', gap: 14, alignItems: 'center', flexWrap: 'wrap' }}>
            <span className="panel-note">
              {hasMistake ? t('practice', 'inMistakes') : t('practice', 'notInMistakes')}
            </span>
            {hasMistake && (
              <button className="ghost-button" onClick={handleMistakeRemove}>
                {t('practice', 'removeMistake')}
              </button>
            )}
            {!hasMistake && (
              <button className="ghost-button" onClick={handleMistakeKeep}>
                {t('practice', 'addMistake')}
              </button>
            )}
          </div>
        </section>
      )}

      {/* Vocabulary pick mode toggle — hidden for translation questions (prompt is Chinese) */}
      {currentQuestion.type !== 'translation' && (
      <section className="panel compact-panel">
        <div className="toolbar-actions" style={{ alignItems: 'center' }}>
          <button
            className={`secondary-button ${vocabPickEnabled ? 'is-active' : ''}`}
            onClick={() => setVocabPickEnabled(!vocabPickEnabled)}
          >
            {vocabPickEnabled ? t('practice', 'vocabOn') : t('practice', 'vocabOff')}
          </button>
          {vocabPickEnabled && (
            <span className="panel-note">
              {t('practice', 'vocabHint')}
            </span>
          )}
        </div>
        {vocabPickEnabled && currentQuestion && (
          <div style={{ marginTop: 14 }}>
            <VocabularyPicker
              text={currentQuestion.prompt}
              enabled={true}
              onPick={handleVocabPick}
            />
          </div>
        )}
      </section>
      )}

      {/* Navigation */}
      <section className="practice-actions">
        <button className="secondary-button" onClick={handlePrev} disabled={currentSession.currentIndex <= 0}>
          {t('practice', 'prev')}
        </button>
        {isLastQuestion ? (
          <Link to="/results" className="primary-button">
            {t('practice', 'results')}
          </Link>
        ) : (
          <button className="primary-button" onClick={handleNext}>
            {t('practice', 'next')}
          </button>
        )}
        <button className="ghost-button" onClick={handleRestart}>
          {t('practice', 'restart')}
        </button>
      </section>
    </div>
  )
}
