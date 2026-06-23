import test from 'node:test'
import assert from 'node:assert/strict'
import {
  createVocabularyRecord,
  mergeVocabularyRecords,
  sanitizeVocabularyRecords,
  tokenizeVocabularyText,
} from './vocabulary.ts'
import type { VocabularyRecord } from '../types.ts'

test('tokenizeVocabularyText keeps molecular biology terms clickable', () => {
  const tokens = tokenizeVocabularyText(
    'Chromatin immunoprecipitation (ChIP) and siRNA-mediated gene silencing.',
  )
  const terms = tokens.filter((token) => token.kind === 'term').map((token) => token.value)

  assert.deepEqual(terms, [
    'Chromatin',
    'immunoprecipitation',
    'ChIP',
    'and',
    'siRNA-mediated',
    'gene',
    'silencing',
  ])
})

test('createVocabularyRecord normalizes the term and preserves source context', () => {
  const record = createVocabularyRecord({
    term: ' ChIP ',
    contextText: 'Chromatin immunoprecipitation (ChIP) is a powerful technique.',
    sourceType: 'practice',
    questionId: 'translation-4-q-015',
    questionNumber: 15,
    chapterId: 4,
    chapterTitle: '分子克隆与实验技术',
  })

  assert.equal(record.term, 'ChIP')
  assert.equal(record.normalizedTerm, 'chip')
  assert.equal(record.status, 'new')
  assert.equal(record.sourceType, 'practice')
  assert.equal(record.questionId, 'translation-4-q-015')
  assert.match(record.id, /^chip-practice-translation-4-q-015-/)
})

test('sanitizeVocabularyRecords removes invalid entries and sorts newest first', () => {
  const records = sanitizeVocabularyRecords([
    {
      id: 'old',
      term: 'chromatin',
      normalizedTerm: 'chromatin',
      contextText: 'chromatin context',
      sourceType: 'practice',
      questionNumber: 1,
      status: 'learning',
      addedAt: '2026-06-13T00:00:00.000Z',
      updatedAt: '2026-06-13T00:00:00.000Z',
    },
    { id: 'bad', term: ' ', normalizedTerm: '', contextText: '', sourceType: 'practice' },
    {
      id: 'new',
      term: 'nucleosome',
      normalizedTerm: 'nucleosome',
      contextText: 'nucleosome context',
      sourceType: 'past-exam',
      examId: 'midterm-25',
      questionNumber: 2,
      status: 'mastered',
      addedAt: '2026-06-14T00:00:00.000Z',
      updatedAt: '2026-06-14T00:00:00.000Z',
    },
  ] as VocabularyRecord[])

  assert.equal(records.length, 2)
  assert.equal(records[0].id, 'new')
  assert.equal(records[1].id, 'old')
})

test('mergeVocabularyRecords deduplicates by normalized term and source', () => {
  const existing = [
    {
      ...createVocabularyRecord({
        term: 'Chromatin',
        contextText: 'chromatin structure',
        sourceType: 'practice',
        questionId: 'translation-1-q-001',
        questionNumber: 1,
      }),
      addedAt: '2026-06-13T00:00:00.000Z',
      updatedAt: '2026-06-13T00:00:00.000Z',
    },
  ]
  const imported = [
    {
      ...existing[0],
      id: 'different-id',
      term: 'chromatin',
      status: 'mastered',
      updatedAt: '2026-06-14T00:00:00.000Z',
    },
    createVocabularyRecord({
      term: 'Nucleosome',
      contextText: 'nucleosome positioning',
      sourceType: 'past-exam',
      examId: 'midterm-25',
      questionNumber: 3,
    }),
  ] as VocabularyRecord[]

  const merged = mergeVocabularyRecords(existing, imported)
  const chromatin = merged.find((record) => record.normalizedTerm === 'chromatin')
  const nucleosome = merged.find((record) => record.normalizedTerm === 'nucleosome')

  assert.equal(merged.length, 2)
  assert.equal(chromatin?.status, 'mastered')
  assert.equal(nucleosome?.sourceType, 'past-exam')
})
