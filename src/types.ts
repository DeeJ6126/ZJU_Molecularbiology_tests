// ── Question type taxonomy ──────────────────────────────────────────

export type QuestionType =
  | 'translation'
  | 'true-false'
  | 'multiple-choice'
  | 'short-answer'
  | 'essay'

// ── Question category (replaces ChapterMeta) ──────────────────────

export interface QuestionCategory {
  id: string
  type: QuestionType
  title: string
  parentTitle?: string
  questionCount: number
}

// ── Multiple choice primitives ────────────────────────────────────

export type OptionKey = 'A' | 'B' | 'C' | 'D'
export type AnswerSelection = OptionKey | 'UNKNOWN'

export interface QuestionOption {
  key: OptionKey
  text: string
  /** Chinese option text for zh language mode */
  textCn?: string
}

// ── AI explanation ────────────────────────────────────────────────

export interface AiExplanation {
  model: string
  generatedAt: string
  explanation: string
  optionExplanations?: Record<string, string>
  confidence?: number
}

// ── Question interfaces (discriminated union) ─────────────────────

interface BaseQuestionFields {
  id: string
  type: QuestionType
  categoryId: string
  categoryTitle: string
  parentTitle?: string
  number: number
  /** Which exam papers this question appeared in (e.g. ['21春夏', '22春夏']) */
  examSources?: string[]
  prompt: string
  /** Chinese prompt for zh language mode */
  promptCn?: string
  /** Chinese explanation for zh language mode (T/F + MC) */
  explanationCn?: string
  aiExplanation?: AiExplanation
}

/** Chinese-English term translation question */
export interface TranslationQuestion extends BaseQuestionFields {
  type: 'translation'
  direction: 'en-to-zh' | 'zh-to-en'
  answerTerm: string
  answerFullTerm?: string
  acceptableAnswers: string[]
  chineseMeaning?: string
}

/** True/False question with built-in explanation */
export interface TrueFalseQuestion extends BaseQuestionFields {
  type: 'true-false'
  answerIsTrue: boolean
  explanation: string
}

/** Multiple choice question (A/B/C/D) */
export interface MultipleChoiceQuestion extends BaseQuestionFields {
  type: 'multiple-choice'
  options: QuestionOption[]
  answerKey: OptionKey | null   // null when distractors not yet generated
  answerText?: string            // raw answer text from DOCX
  explanation: string
  distractorsGenerated: boolean
}

/** Short answer with self-judge and reference answer reveal */
export interface ShortAnswerQuestion extends BaseQuestionFields {
  type: 'short-answer'
  referenceAnswer: string
}

/** Essay/analysis question with self-judge */
export interface EssayQuestion extends BaseQuestionFields {
  type: 'essay'
  referenceAnswer: string
}

export type Question =
  | TranslationQuestion
  | TrueFalseQuestion
  | MultipleChoiceQuestion
  | ShortAnswerQuestion
  | EssayQuestion

// ── Question bank ─────────────────────────────────────────────────

export interface QuestionBank {
  generatedAt: string
  totalQuestions: number
  categories: QuestionCategory[]
  questions: Question[]
}

// ── Practice session ──────────────────────────────────────────────

export type PracticeMode = 'categories' | 'mistakes'

export interface PracticeAnswer {
  questionId: string
  selectedKey?: AnswerSelection
  textAnswer?: string
  selfJudgedCorrect?: boolean
  isCorrect: boolean
  answeredAt: string
}

export interface PracticeSession {
  mode: PracticeMode
  title: string
  selectedCategoryIds: string[]
  questionOrder: string[]
  currentIndex: number
  answers: PracticeAnswer[]
  startedAt: string
}

// ── Mistake records ───────────────────────────────────────────────

export interface MistakeRecord {
  questionId: string
  questionType: QuestionType
  categoryId: string
  lastSelectedKey?: AnswerSelection
  lastTextAnswer?: string
  correctAnswerDisplay: string
  wrongCount: number
  lastAnsweredAt: string
}

// ── Vocabulary (unchanged from Microbiology platform) ─────────────

export type VocabularySourceType = 'practice' | 'past-exam'

export type VocabularyStatus = 'new' | 'learning' | 'mastered'

export interface VocabularyRecord {
  id: string
  term: string
  normalizedTerm: string
  contextText: string
  sourceType: VocabularySourceType
  questionId?: string
  examId?: string
  questionNumber: number
  chapterId?: number
  chapterTitle?: string
  status: VocabularyStatus
  addedAt: string
  updatedAt: string
}

export interface VocabularyRecordInput {
  term: string
  contextText: string
  sourceType: VocabularySourceType
  questionId?: string
  examId?: string
  questionNumber: number
  chapterId?: number
  chapterTitle?: string
}
