import { Link } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'
import { FlashcardReview } from '../components/FlashcardReview'
import { useT } from '../lib/i18n'
import type { TranslationQuestion } from '../types'

export function ReviewPage() {
  const practice = usePractice()
  const t = useT()
  const { questionBank, selectedCategoryIds } = practice

  // Filter translation questions from selected categories
  const translationQuestions = questionBank.questions.filter(
    (q): q is TranslationQuestion =>
      q.type === 'translation' && selectedCategoryIds.includes(q.categoryId),
  )

  if (!selectedCategoryIds.length) {
    return (
      <div className="page-stack">
        <section className="panel empty-state">
          <h2>{t('review', 'noSelection')}</h2>
          <p>{t('review', 'noSelectionHint')}</p>
          <Link to="/categories" className="primary-button" style={{ marginTop: 16 }}>
            {t('review', 'goToCategories')}
          </Link>
        </section>
      </div>
    )
  }

  if (!translationQuestions.length) {
    return (
      <div className="page-stack">
        <section className="panel empty-state">
          <h2>{t('review', 'noTranslation')}</h2>
          <p>
            {t('review', 'noTranslationHint')}
          </p>
          <Link to="/categories" className="primary-button" style={{ marginTop: 16 }}>
            {t('review', 'goToCategories')}
          </Link>
        </section>
      </div>
    )
  }

  return <FlashcardReview questions={translationQuestions} />
}
