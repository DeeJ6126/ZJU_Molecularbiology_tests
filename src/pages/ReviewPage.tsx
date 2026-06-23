import { Link } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'
import { FlashcardReview } from '../components/FlashcardReview'
import type { TranslationQuestion } from '../types'

export function ReviewPage() {
  const practice = usePractice()
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
          <h2>未选择题型</h2>
          <p>请先在题型选择页勾选包含翻译题的子分类。</p>
          <Link to="/categories" className="primary-button" style={{ marginTop: 16 }}>
            前往题型选择
          </Link>
        </section>
      </div>
    )
  }

  if (!translationQuestions.length) {
    return (
      <div className="page-stack">
        <section className="panel empty-state">
          <h2>没有翻译题</h2>
          <p>
            当前选中的子分类中不包含中英名词互译题。请在题型选择页勾选翻译题子分类后再试。
          </p>
          <Link to="/categories" className="primary-button" style={{ marginTop: 16 }}>
            前往题型选择
          </Link>
        </section>
      </div>
    )
  }

  return <FlashcardReview questions={translationQuestions} />
}
