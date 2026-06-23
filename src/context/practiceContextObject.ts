import { createContext } from 'react'
import type {
  AnswerSelection,
  MistakeRecord,
  PracticeSession,
  Question,
  QuestionBank,
  VocabularyRecord,
  VocabularyRecordInput,
  VocabularyStatus,
} from '../types'

export interface PracticeContextValue {
  questionBank: QuestionBank
  session: PracticeSession | null
  selectedCategoryIds: string[]
  mistakeRecords: MistakeRecord[]
  vocabularyRecords: VocabularyRecord[]
  setSelectedCategoryIds: (categoryIds: string[]) => void
  beginPractice: (categoryIds: string[]) => PracticeSession | null
  beginMistakePractice: () => PracticeSession | null
  restartPractice: () => PracticeSession | null
  /** Record a multiple-choice or true-false answer */
  recordAnswer: (questionId: string, selectedKey: AnswerSelection) => void
  /** Record a translation text answer */
  recordTextAnswer: (questionId: string, textAnswer: string) => void
  /** Record self-judgment for short-answer / essay */
  recordSelfJudge: (questionId: string, isCorrect: boolean) => void
  goToIndex: (index: number) => void
  clearSession: () => void
  keepMistake: (questionId: string, selectedKey?: AnswerSelection, textAnswer?: string) => void
  removeMistake: (questionId: string) => void
  clearMistakes: () => void
  hasMistake: (questionId: string) => boolean
  addVocabularyRecord: (input: VocabularyRecordInput) => VocabularyRecord | null
  removeVocabularyRecord: (recordId: string) => void
  updateVocabularyRecordStatus: (recordId: string, status: VocabularyStatus) => void
  clearVocabularyRecords: () => void
  importVocabularyRecords: (records: VocabularyRecord[]) => void
  getQuestionById: (questionId: string) => Question | undefined
}

export const PracticeContext = createContext<PracticeContextValue | null>(null)
