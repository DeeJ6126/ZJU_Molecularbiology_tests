import { Link, useNavigate } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'
import { getSubcategories, getQuestionTypes } from '../lib/categoryScope'
import type { QuestionType } from '../types'

const TYPE_LABELS: Record<QuestionType, string> = {
  translation: '中英名词互译',
  'true-false': '判断题',
  'multiple-choice': '选择题',
  'short-answer': '简答题',
  essay: '分析论述题',
}

const TYPE_ORDER: QuestionType[] = [
  'translation',
  'true-false',
  'multiple-choice',
  'short-answer',
  'essay',
]

export function CategorySelectionPage() {
  const navigate = useNavigate()
  const practice = usePractice()
  const { questionBank, selectedCategoryIds, setSelectedCategoryIds, beginPractice } = practice

  const types = getQuestionTypes(questionBank).sort(
    (a, b) => TYPE_ORDER.indexOf(a) - TYPE_ORDER.indexOf(b),
  )

  function toggleCategory(categoryId: string) {
    if (selectedCategoryIds.includes(categoryId)) {
      setSelectedCategoryIds(selectedCategoryIds.filter((id) => id !== categoryId))
    } else {
      setSelectedCategoryIds([...selectedCategoryIds, categoryId])
    }
  }

  function selectAllInType(type: QuestionType) {
    const subIds = getSubcategories(questionBank, type).map((c) => c.id)
    const others = selectedCategoryIds.filter(
      (id) => !subIds.includes(id),
    )
    setSelectedCategoryIds([...others, ...subIds])
  }

  function clearType(type: QuestionType) {
    const subIds = new Set(getSubcategories(questionBank, type).map((c) => c.id))
    setSelectedCategoryIds(selectedCategoryIds.filter((id) => !subIds.has(id)))
  }

  function handleStart() {
    if (!selectedCategoryIds.length) return
    beginPractice(selectedCategoryIds)
    navigate('/practice')
  }

  const totalSelected = questionBank.categories
    .filter((c) => selectedCategoryIds.includes(c.id))
    .reduce((sum, c) => sum + c.questionCount, 0)

  return (
    <div className={`page-stack ${selectedCategoryIds.length > 0 ? 'page-with-dock' : ''}`}>
      <section className="panel compact-panel">
        <div className="section-heading">
          <div>
            <h2>选择题型与子分类</h2>
            <p className="scope-note">
              按题型勾选想练习的子分类。已选 <strong>{totalSelected}</strong> 题。
            </p>
          </div>
          {selectedCategoryIds.length > 0 && (
            <button
              className="primary-button desktop-only"
              onClick={handleStart}
            >
              开始练习（{totalSelected} 题）
            </button>
          )}
        </div>
      </section>

      {types.map((type) => {
        const subcategories = getSubcategories(questionBank, type)
        if (!subcategories.length) return null

        const selectedInType = subcategories.filter((c) =>
          selectedCategoryIds.includes(c.id),
        )
        const allSelected = selectedInType.length === subcategories.length

        return (
          <section key={type} className="panel compact-panel">
            <div className="section-heading">
              <h2>{TYPE_LABELS[type] || type}</h2>
              <div className="toolbar-actions">
                {type === 'translation' && selectedInType.length > 0 && (
                  <Link to="/review" className="secondary-button" style={{ textDecoration: 'none' }}>
                    复习模式
                  </Link>
                )}
                <button
                  className="ghost-button"
                  onClick={() =>
                    allSelected ? clearType(type) : selectAllInType(type)
                  }
                >
                  {allSelected ? '取消全选' : '全选'}
                </button>
                {selectedInType.length > 0 && (
                  <button className="ghost-button" onClick={() => clearType(type)}>
                    清空
                  </button>
                )}
              </div>
            </div>

            <div className="chapter-grid">
              {subcategories.map((cat) => {
                const isSelected = selectedCategoryIds.includes(cat.id)
                return (
                  <button
                    key={cat.id}
                    className={`chapter-card ${isSelected ? 'is-selected' : ''}`}
                    onClick={() => toggleCategory(cat.id)}
                    type="button"
                  >
                    <div className="chapter-card-top">
                      <span className="chapter-chip">{cat.title}</span>
                      <span className="chapter-count">{cat.questionCount} 题</span>
                    </div>
                  </button>
                )
              })}
            </div>
          </section>
        )
      })}

      {/* Mobile dock */}
      {selectedCategoryIds.length > 0 && (
        <div className="mobile-dock">
          <div className="mobile-dock-copy">
            <strong>已选 {totalSelected} 题</strong>
          </div>
          <button className="primary-button" onClick={handleStart}>
            开始练习
          </button>
        </div>
      )}
    </div>
  )
}
