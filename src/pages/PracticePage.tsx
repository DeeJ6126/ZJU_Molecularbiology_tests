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
import type { AnswerSelection, VocabularySourceType } from '../types'

export function PracticePage() {
  const navigate = useNavigate()
  const practice = usePractice()
  const { questionBank, session, vocabularyRecords, addVocabularyRecord } =
    practice

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
          <p>题库中找不到当前题目。</p>
          <button
            className="primary-button"
            onClick={() => {
              practice.clearSession()
              navigate('/categories')
            }}
          >
            返回题型选择
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
    translation: '中英名词互译',
    'true-false': '判断题',
    'multiple-choice': '选择题',
    'short-answer': '简答题',
    essay: '分析论述题',
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
          第 {currentSession.currentIndex + 1} / {currentSession.questionOrder.length} 题
        </span>
        {isMistakeMode && (
          <span className="status-pill" style={{ background: 'var(--coral-soft)', color: '#8c4d29' }}>
            错题复习
          </span>
        )}
      </div>

      {/* Question prompt (with optional vocabulary picker) */}
      <div className="panel compact-panel">
        <div className="question-meta" style={{ marginBottom: 12 }}>
          <span className="panel-note">#{currentQuestion.number}</span>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: 8, alignItems: 'center' }}>
            <VocabularyPicker
              text={currentQuestion.prompt}
              enabled={false}
              onPick={() => {}}
            />
          </div>
        </div>
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
              {hasMistake ? '此题在错题本中' : '此题不在错题本中'}
            </span>
            {hasMistake && (
              <button className="ghost-button" onClick={handleMistakeRemove}>
                从错题本移除
              </button>
            )}
            {!hasMistake && (
              <button className="ghost-button" onClick={handleMistakeKeep}>
                加入错题本
              </button>
            )}
          </div>
        </section>
      )}

      {/* Vocabulary pick mode toggle */}
      <section className="panel compact-panel">
        <div className="toolbar-actions" style={{ alignItems: 'center' }}>
          <button
            className={`secondary-button ${vocabPickEnabled ? 'is-active' : ''}`}
            onClick={() => setVocabPickEnabled(!vocabPickEnabled)}
          >
            {vocabPickEnabled ? '✓ 取词模式开' : '生词取词模式'}
          </button>
          {vocabPickEnabled && (
            <span className="panel-note">
              点击题目中的英文单词即可收入生词本
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

      {/* Navigation */}
      <section className="practice-actions">
        <button className="secondary-button" onClick={handlePrev} disabled={currentSession.currentIndex <= 0}>
          上一题
        </button>
        {isLastQuestion ? (
          <Link to="/results" className="primary-button">
            查看结果
          </Link>
        ) : (
          <button className="primary-button" onClick={handleNext}>
            下一题
          </button>
        )}
        <button className="ghost-button" onClick={handleRestart}>
          重新开始
        </button>
      </section>
    </div>
  )
}
