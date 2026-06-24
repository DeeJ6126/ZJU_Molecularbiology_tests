import type {
  MistakeRecord,
  PracticeAnswer,
  PracticeMode,
  PracticeSession,
  Question,
  QuestionBank,
  TranslationQuestion,
} from '../types'
import { getAllCategoryIds } from './categoryScope'

// ── Category selection ────────────────────────────────────────────

export function normalizeCategorySelection(
  categoryIds: string[],
  questionBank: QuestionBank,
): string[] {
  const allowed = new Set(getAllCategoryIds(questionBank))
  const uniqueIds = Array.from(new Set(categoryIds))

  return uniqueIds
    .filter((id) => allowed.has(id))
    .sort()
}

// ── Question pool ─────────────────────────────────────────────────

export function getPracticePool(
  questionBank: QuestionBank,
  categoryIds: string[],
): Question[] {
  const selected = new Set(categoryIds)
  return questionBank.questions.filter((question) =>
    selected.has(question.categoryId),
  )
}

// ── Session creation ──────────────────────────────────────────────

export function createPracticeSession(
  categoryIds: string[],
  questionBank: QuestionBank,
): PracticeSession | null {
  const selectedCategoryIds = normalizeCategorySelection(categoryIds, questionBank)

  if (!selectedCategoryIds.length) {
    return null
  }

  const pool = getPracticePool(questionBank, selectedCategoryIds)

  return buildPracticeSession({
    mode: 'categories',
    title: buildSessionTitle(selectedCategoryIds, questionBank),
    selectedCategoryIds,
    questionIds: pool.map((q) => q.id),
  })
}

export function createMistakePracticeSession(
  mistakeRecords: MistakeRecord[],
  questionBank: QuestionBank,
): PracticeSession | null {
  const mistakeQuestionIds = Array.from(
    new Set(mistakeRecords.map((record) => record.questionId)),
  )

  if (!mistakeQuestionIds.length) {
    return null
  }

  // Collect category IDs from mistake questions
  const selectedCategoryIds = normalizeCategorySelection(
    Array.from(
      new Set(
        mistakeQuestionIds
          .map((id) => questionBank.questions.find((q) => q.id === id))
          .filter((q): q is Question => Boolean(q))
          .map((q) => q.categoryId),
      ),
    ),
    questionBank,
  )

  return buildPracticeSession({
    mode: 'mistakes',
    title: '错题本练习',
    selectedCategoryIds,
    questionIds: mistakeQuestionIds,
  })
}

function buildPracticeSession({
  mode,
  title,
  selectedCategoryIds,
  questionIds,
}: {
  mode: PracticeMode
  title: string
  selectedCategoryIds: string[]
  questionIds: string[]
}): PracticeSession | null {
  if (!questionIds.length) {
    return null
  }

  return {
    mode,
    title,
    selectedCategoryIds,
    questionOrder: shuffleArray(questionIds),
    currentIndex: 0,
    answers: [],
    startedAt: new Date().toISOString(),
  }
}

function buildSessionTitle(
  categoryIds: string[],
  questionBank: QuestionBank,
): string {
  if (categoryIds.length === 1) {
    const category = questionBank.categories.find((c) => c.id === categoryIds[0])
    const name = category
      ? `${category.parentTitle || ''} · ${category.title}`
      : '单类练习'
    return name
  }

  // Count by type
  const types = new Set<string>()
  for (const cid of categoryIds) {
    const cat = questionBank.categories.find((c) => c.id === cid)
    if (cat) types.add(cat.parentTitle || cat.type)
  }

  return `${categoryIds.length} 个分类混练`
}

// ── Question lookup ───────────────────────────────────────────────

export function buildQuestionLookup(
  questionBank: QuestionBank,
): Record<string, Question> {
  const lookup: Record<string, Question> = {}
  for (const question of questionBank.questions) {
    lookup[question.id] = question
  }
  return lookup
}

export function findAnswer(
  session: PracticeSession | null,
  questionId: string,
): PracticeAnswer | undefined {
  return session?.answers.find((answer) => answer.questionId === questionId)
}

// ── Scoring ───────────────────────────────────────────────────────

export function getScoreSummary(session: PracticeSession | null) {
  const total = session?.questionOrder.length ?? 0
  const answered = session?.answers.length ?? 0
  const correct =
    session?.answers.filter((answer) => answer.isCorrect).length ?? 0
  const selfJudgedCorrect =
    session?.answers.filter((answer) => answer.selfJudgedCorrect === true).length ?? 0
  const selfJudgedIncorrect =
    session?.answers.filter((answer) => answer.selfJudgedCorrect === false).length ?? 0
  const unanswered = Math.max(total - answered, 0)
  const accuracy = total ? Math.round((correct / total) * 100) : 0

  return {
    total,
    answered,
    correct,
    selfJudgedCorrect,
    selfJudgedIncorrect,
    unanswered,
    accuracy,
  }
}

// ── Translation abbreviation matching ─────────────────────────────

/**
 * Check a user's text answer against a translation question's acceptable answers.
 *
 * Matching rules:
 * 1. Normalize both input and answers (trim, lowercase, collapse whitespace)
 * 2. Exact match against any acceptable answer → correct
 * 3. Singular/plural tolerant: "Prokaryote" matches "Prokaryotes"
 * 4. Abbreviation-only match: if answer has "ChIP (Chromatin immunoprecipitation)",
 *    accepting "ChIP" or "Chromatin immunoprecipitation" individually.
 */
export function checkTranslationAnswer(
  userInput: string,
  question: TranslationQuestion,
): boolean {
  const normalized = normalizeAnswerText(userInput)
  if (!normalized) return false

  // Collect all acceptable forms: explicit acceptableAnswers + abbreviation
  const allAcceptable: string[] = [...question.acceptableAnswers]
  if (question.answerFullTerm) {
    allAcceptable.push(question.answerFullTerm)
  }

  // Exact match
  if (allAcceptable.some(
    (answer) => normalizeAnswerText(answer) === normalized,
  )) {
    return true
  }

  // Singular/plural tolerant match: generate possible stems for both
  // input and answer, then check if any pair matches.
  const inputStems = getPossibleStems(normalized)
  return allAcceptable.some((answer) => {
    const answerStems = getPossibleStems(normalizeAnswerText(answer))
    return inputStems.some((is) => answerStems.includes(is))
  })
}

function normalizeAnswerText(text: string): string {
  return text
    .trim()
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/[，,。\.！!？?；;：:、\s()（）\[\]【】]+$/, '')  // trailing punctuation
    .replace(/^[，,。\.！!？?；;：:、\s()（）\[\]【】]+/, '')  // leading punctuation
}

/**
 * Generate possible singular/plural stems for matching.
 * Returns the original word plus plausible de-pluralized variants.
 *
 * For "prokaryotes": ["prokaryotes", "prokaryote"] (strip -s only, -es is too aggressive)
 * For "boxes":       ["boxes", "boxe", "box"]        (tries both -s and -es)
 * For "bodies":      ["bodies", "body"]               (-ies → -y)
 */
function getPossibleStems(word: string): string[] {
  const stems = new Set<string>()
  stems.add(word) // always include original

  if (word.length <= 2) return Array.from(stems)

  // -ies → -y (bodies → body)
  if (word.endsWith('ies') && word.length > 4) {
    stems.add(word.slice(0, -3) + 'y')
  }

  // -ves → -f (lives → life)
  if (word.endsWith('ves') && word.length > 4) {
    stems.add(word.slice(0, -3) + 'f')
  }

  // -es → "" (boxes → box), but also try -s alone
  if (word.endsWith('es') && word.length > 4) {
    stems.add(word.slice(0, -2))  // drop -es
  }

  // -s → "" (prokaryotes → prokaryote)
  if (word.endsWith('s') && word.length > 3) {
    stems.add(word.slice(0, -1))  // drop -s only
  }

  return Array.from(stems)
}

// ── Answer display ────────────────────────────────────────────────

/**
 * Return a human-readable string representing the correct answer for a question.
 * Used for mistake record display.
 */
export function getAnswerDisplay(question: Question): string {
  switch (question.type) {
    case 'translation': {
      if (question.direction === 'zh-to-en') {
        const parts: string[] = [question.answerTerm]
        if (question.answerFullTerm && question.answerFullTerm !== question.answerTerm) {
          parts.push(`(${question.answerFullTerm})`)
        }
        return parts.join(' ')
      }
      return question.chineseMeaning || question.answerTerm
    }

    case 'true-false':
      return question.answerIsTrue ? '正确' : '错误'

    case 'multiple-choice': {
      if (question.answerKey) {
        const option = question.options.find((o) => o.key === question.answerKey)
        return option ? `${question.answerKey}. ${option.text}` : question.answerKey
      }
      return question.answerText || '答案待生成'
    }

    case 'short-answer':
    case 'essay':
      return question.referenceAnswer.slice(0, 200) + (
        question.referenceAnswer.length > 200 ? '...' : ''
      )

    default:
      return ''
  }
}

// ── Utilities ─────────────────────────────────────────────────────

export function shuffleArray<T>(items: T[]): T[] {
  const nextItems = [...items]

  for (let index = nextItems.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(Math.random() * (index + 1))
    ;[nextItems[index], nextItems[swapIndex]] = [
      nextItems[swapIndex],
      nextItems[index],
    ]
  }

  return nextItems
}
