import { useEffect, useState } from 'react'
import type { PropsWithChildren } from 'react'
import {
  buildQuestionLookup,
  checkTranslationAnswer,
  createMistakePracticeSession,
  createPracticeSession,
  getAnswerDisplay,
  getPracticePool,
  normalizeCategorySelection,
} from '../lib/practice'
import {
  createVocabularyRecord,
  getVocabularyDedupeKey,
  mergeVocabularyRecords,
  sanitizeVocabularyRecords,
  updateVocabularyStatus,
} from '../lib/vocabulary'
import { PracticeContext } from './practiceContextObject'
import type {
  AnswerSelection,
  MistakeRecord,
  PracticeSession,
  Question,
  QuestionBank,
  QuestionType,
  TranslationQuestion,
  VocabularyRecord,
  VocabularyRecordInput,
  VocabularyStatus,
} from '../types'

const SESSION_STORAGE_KEY = 'molecular-biology-session'
const SELECTION_STORAGE_KEY = 'molecular-biology-selection'
const MISTAKES_STORAGE_KEY = 'molecular-biology-mistakes'
const VOCABULARY_STORAGE_KEY = 'molecular-biology-vocabulary'

export function PracticeProvider({
  children,
  questionBank,
}: PropsWithChildren<{ questionBank: QuestionBank }>) {
  const questionLookup = buildQuestionLookup(questionBank)

  const [selectedCategoryIds, setSelectedCategoryIdsState] = useState<string[]>(
    () =>
      normalizeCategorySelection(
        readStoredValue<string[]>(SELECTION_STORAGE_KEY) ?? [],
        questionBank,
      ),
  )

  const [mistakeRecords, setMistakeRecords] = useState<MistakeRecord[]>(() =>
    sanitizeMistakes(
      readStoredValue<MistakeRecord[]>(MISTAKES_STORAGE_KEY) ?? [],
      questionLookup,
    ),
  )

  const [session, setSession] = useState<PracticeSession | null>(() =>
    sanitizeSession(
      readStoredValue<PracticeSession>(SESSION_STORAGE_KEY),
      questionBank,
      mistakeRecords,
    ),
  )

  const [vocabularyRecords, setVocabularyRecords] = useState<VocabularyRecord[]>(
    () =>
      sanitizeVocabularyRecords(
        readStoredValue<VocabularyRecord[]>(VOCABULARY_STORAGE_KEY) ?? [],
      ),
  )

  // Persist to localStorage
  useEffect(() => {
    writeStoredValue(SELECTION_STORAGE_KEY, selectedCategoryIds)
  }, [selectedCategoryIds])

  useEffect(() => {
    writeStoredValue(MISTAKES_STORAGE_KEY, mistakeRecords)
  }, [mistakeRecords])

  useEffect(() => {
    writeStoredValue(SESSION_STORAGE_KEY, session)
  }, [session])

  useEffect(() => {
    writeStoredValue(VOCABULARY_STORAGE_KEY, vocabularyRecords)
  }, [vocabularyRecords])

  // ── Category selection ─────────────────────────────────────────

  function setSelectedCategoryIds(categoryIds: string[]) {
    setSelectedCategoryIdsState(normalizeCategorySelection(categoryIds, questionBank))
  }

  // ── Practice session ────────────────────────────────────────────

  function beginPractice(categoryIds: string[]) {
    const normalized = normalizeCategorySelection(categoryIds, questionBank)
    const nextSession = createPracticeSession(normalized, questionBank)
    setSelectedCategoryIdsState(normalized)
    setSession(nextSession)
    return nextSession
  }

  function beginMistakePractice() {
    const nextSession = createMistakePracticeSession(mistakeRecords, questionBank)
    setSession(nextSession)
    return nextSession
  }

  function restartPractice() {
    if (session?.mode === 'mistakes') {
      return beginMistakePractice()
    }
    const sourceIds = session?.selectedCategoryIds ?? selectedCategoryIds
    const nextSession = createPracticeSession(sourceIds, questionBank)
    setSession(nextSession)
    return nextSession
  }

  // ── Answer recording ────────────────────────────────────────────

  /** Record multiple-choice or true-false answer. */
  function recordAnswer(questionId: string, selectedKey: AnswerSelection) {
    const question = questionLookup[questionId]
    if (!question) return

    const answeredAt = new Date().toISOString()

    let isCorrect = false
    if (question.type === 'multiple-choice') {
      isCorrect = question.answerKey === selectedKey
    } else if (question.type === 'true-false') {
      const tfCorrect =
        selectedKey === 'UNKNOWN'
          ? false
          : (selectedKey === 'A') === question.answerIsTrue
      isCorrect = tfCorrect
    }

    setSession((current) => {
      if (!current || current.answers.some((a) => a.questionId === questionId)) {
        return current
      }
      return {
        ...current,
        answers: [
          ...current.answers,
          {
            questionId,
            selectedKey,
            isCorrect,
            answeredAt,
          },
        ],
      }
    })

    if (!isCorrect) {
      setMistakeRecords((current) =>
        upsertMistake(current, question, selectedKey, undefined, answeredAt),
      )
    }
  }

  /** Record text answer for translation questions. */
  function recordTextAnswer(questionId: string, textAnswer: string) {
    const question = questionLookup[questionId]
    if (!question || question.type !== 'translation') return

    const answeredAt = new Date().toISOString()
    const isCorrect = checkTranslationAnswer(textAnswer, question as TranslationQuestion)

    setSession((current) => {
      if (!current || current.answers.some((a) => a.questionId === questionId)) {
        return current
      }
      return {
        ...current,
        answers: [
          ...current.answers,
          {
            questionId,
            textAnswer,
            isCorrect,
            answeredAt,
          },
        ],
      }
    })

    if (!isCorrect) {
      setMistakeRecords((current) =>
        upsertMistake(current, question, undefined, textAnswer, answeredAt),
      )
    }
  }

  /** Record self-judgment for short-answer / essay questions. */
  function recordSelfJudge(questionId: string, isCorrect: boolean) {
    const question = questionLookup[questionId]
    if (!question) return
    if (question.type !== 'short-answer' && question.type !== 'essay') return

    const answeredAt = new Date().toISOString()

    setSession((current) => {
      if (!current || current.answers.some((a) => a.questionId === questionId)) {
        return current
      }
      return {
        ...current,
        answers: [
          ...current.answers,
          {
            questionId,
            selfJudgedCorrect: isCorrect,
            isCorrect, // treat self-judged-correct as correct for scoring
            answeredAt,
          },
        ],
      }
    })

    if (!isCorrect) {
      setMistakeRecords((current) =>
        upsertMistake(current, question, undefined, undefined, answeredAt),
      )
    }
  }

  function goToIndex(index: number) {
    setSession((current) => {
      if (!current) return current
      return {
        ...current,
        currentIndex: Math.min(
          Math.max(index, 0),
          Math.max(current.questionOrder.length - 1, 0),
        ),
      }
    })
  }

  function clearSession() {
    setSession(null)
  }

  // ── Mistake management ──────────────────────────────────────────

  function removeMistake(questionId: string) {
    setMistakeRecords((current) =>
      current.filter((record) => record.questionId !== questionId),
    )
  }

  function keepMistake(
    questionId: string,
    selectedKey?: AnswerSelection,
    textAnswer?: string,
  ) {
    const question = questionLookup[questionId]
    if (!question) return

    const answeredAt = new Date().toISOString()
    setMistakeRecords((current) =>
      keepMistakeRecord(current, question, selectedKey, textAnswer, answeredAt),
    )
  }

  function clearMistakes() {
    setMistakeRecords([])
  }

  function hasMistake(questionId: string) {
    return mistakeRecords.some((record) => record.questionId === questionId)
  }

  // ── Vocabulary ──────────────────────────────────────────────────

  function addVocabularyRecord(input: VocabularyRecordInput) {
    const nextRecord = createVocabularyRecord(input)
    if (!nextRecord.term || !nextRecord.normalizedTerm) return null
    setVocabularyRecords((current) => upsertVocabularyRecord(current, nextRecord))
    return nextRecord
  }

  function removeVocabularyRecord(recordId: string) {
    setVocabularyRecords((current) =>
      current.filter((record) => record.id !== recordId),
    )
  }

  function updateVocabularyRecordStatus(recordId: string, status: VocabularyStatus) {
    setVocabularyRecords((current) =>
      updateVocabularyStatus(current, recordId, status),
    )
  }

  function clearVocabularyRecords() {
    setVocabularyRecords([])
  }

  function importVocabularyRecords(records: VocabularyRecord[]) {
    setVocabularyRecords((current) => mergeVocabularyRecords(current, records))
  }

  return (
    <PracticeContext.Provider
      value={{
        questionBank,
        session,
        selectedCategoryIds,
        mistakeRecords,
        vocabularyRecords,
        setSelectedCategoryIds,
        beginPractice,
        beginMistakePractice,
        restartPractice,
        recordAnswer,
        recordTextAnswer,
        recordSelfJudge,
        goToIndex,
        clearSession,
        keepMistake,
        removeMistake,
        clearMistakes,
        hasMistake,
        addVocabularyRecord,
        removeVocabularyRecord,
        updateVocabularyRecordStatus,
        clearVocabularyRecords,
        importVocabularyRecords,
        getQuestionById: (questionId: string) => questionLookup[questionId],
      }}
    >
      {children}
    </PracticeContext.Provider>
  )
}

// ── Sanitization ──────────────────────────────────────────────────

function sanitizeSession(
  session: PracticeSession | null,
  questionBank: QuestionBank,
  mistakeRecords: MistakeRecord[],
): PracticeSession | null {
  if (!session) return null

  if (session.mode === 'mistakes') {
    const validIds = new Set(mistakeRecords.map((r) => r.questionId))
    const questionOrder = session.questionOrder.filter((id) => validIds.has(id))
    const selectedCategoryIds = normalizeCategorySelection(
      Array.from(
        new Set(
          mistakeRecords
            .map((r) => questionBank.questions.find((q) => q.id === r.questionId))
            .filter((q): q is Question => Boolean(q))
            .map((q) => q.categoryId),
        ),
      ),
      questionBank,
    )

    if (!questionOrder.length) {
      return createMistakePracticeSession(mistakeRecords, questionBank)
    }

    return {
      ...session,
      mode: 'mistakes',
      title: session.title || '错题本练习',
      selectedCategoryIds,
      questionOrder,
      currentIndex: Math.min(session.currentIndex, questionOrder.length - 1),
      answers: session.answers
        .filter((a) => validIds.has(a.questionId))
        .map((a) => ({ ...a, answeredAt: a.answeredAt || session.startedAt })),
    }
  }

  const selectedCategoryIds = normalizeCategorySelection(
    session.selectedCategoryIds,
    questionBank,
  )

  if (!selectedCategoryIds.length) return null

  const validIds = new Set(
    getPracticePool(questionBank, selectedCategoryIds).map((q) => q.id),
  )

  const questionOrder = session.questionOrder.filter((id) => validIds.has(id))

  if (!questionOrder.length) {
    return createPracticeSession(selectedCategoryIds, questionBank)
  }

  return {
    ...session,
    mode: 'categories',
    title: session.title || '题型混练',
    selectedCategoryIds,
    questionOrder,
    currentIndex: Math.min(session.currentIndex, questionOrder.length - 1),
    answers: session.answers
      .filter((a) => validIds.has(a.questionId))
      .map((a) => ({ ...a, answeredAt: a.answeredAt || session.startedAt })),
  }
}

function sanitizeMistakes(
  records: MistakeRecord[],
  questionLookup: Record<string, Question>,
): MistakeRecord[] {
  const result: MistakeRecord[] = []

  for (const record of records) {
    const question = questionLookup[record.questionId]
    if (!question) continue

    result.push({
      questionId: record.questionId,
      questionType: (record.questionType || question.type) as QuestionType,
      categoryId: record.categoryId || question.categoryId,
      lastSelectedKey: record.lastSelectedKey,
      lastTextAnswer: record.lastTextAnswer,
      correctAnswerDisplay:
        record.correctAnswerDisplay || getAnswerDisplay(question),
      wrongCount: Math.max(record.wrongCount ?? 1, 1),
      lastAnsweredAt: record.lastAnsweredAt || new Date().toISOString(),
    })
  }

  result.sort((left, right) => right.lastAnsweredAt.localeCompare(left.lastAnsweredAt))
  return result
}

// ── Mistake upsert ───────────────────────────────────────────────

function upsertMistake(
  records: MistakeRecord[],
  question: Question,
  selectedKey: AnswerSelection | undefined,
  textAnswer: string | undefined,
  answeredAt: string,
): MistakeRecord[] {
  const existing = records.find((r) => r.questionId === question.id)
  const display = getAnswerDisplay(question)

  const record: MistakeRecord = {
    questionId: question.id,
    questionType: question.type,
    categoryId: question.categoryId,
    lastSelectedKey: selectedKey,
    lastTextAnswer: textAnswer,
    correctAnswerDisplay: display,
    wrongCount: existing ? existing.wrongCount + 1 : 1,
    lastAnsweredAt: answeredAt,
  }

  return [record, ...records.filter((r) => r.questionId !== question.id)]
}

function keepMistakeRecord(
  records: MistakeRecord[],
  question: Question,
  selectedKey: AnswerSelection | undefined,
  textAnswer: string | undefined,
  answeredAt: string,
): MistakeRecord[] {
  const existing = records.find((r) => r.questionId === question.id)
  const display = getAnswerDisplay(question)

  const record: MistakeRecord = {
    questionId: question.id,
    questionType: question.type,
    categoryId: question.categoryId,
    lastSelectedKey: selectedKey,
    lastTextAnswer: textAnswer,
    correctAnswerDisplay: display,
    wrongCount: existing ? existing.wrongCount : 1,
    lastAnsweredAt: answeredAt,
  }

  return [record, ...records.filter((r) => r.questionId !== question.id)]
}

// ── Vocabulary upsert ─────────────────────────────────────────────

function upsertVocabularyRecord(
  records: VocabularyRecord[],
  nextRecord: VocabularyRecord,
): VocabularyRecord[] {
  const nextKey = getVocabularyDedupeKey(nextRecord)
  const existing = records.find((r) => getVocabularyDedupeKey(r) === nextKey)

  if (!existing) {
    return [nextRecord, ...records]
  }

  return [
    {
      ...existing,
      term: nextRecord.term,
      contextText: nextRecord.contextText,
      updatedAt: nextRecord.updatedAt,
    },
    ...records.filter((r) => r.id !== existing.id),
  ]
}

// ── Storage helpers ───────────────────────────────────────────────

function readStoredValue<T>(key: string): T | null {
  if (typeof window === 'undefined') return null
  try {
    const rawValue = window.localStorage.getItem(key)
    return rawValue ? (JSON.parse(rawValue) as T) : null
  } catch {
    return null
  }
}

function writeStoredValue(key: string, value: unknown) {
  if (typeof window === 'undefined') return
  try {
    if (value === null) {
      window.localStorage.removeItem(key)
      return
    }
    window.localStorage.setItem(key, JSON.stringify(value))
  } catch {
    window.localStorage.removeItem(key)
  }
}
