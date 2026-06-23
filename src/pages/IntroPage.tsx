import { Link } from 'react-router-dom'
import { usePractice } from '../hooks/usePractice'
import { getQuestionTypes } from '../lib/categoryScope'

export function IntroPage() {
  const practice = usePractice()
  const types = getQuestionTypes(practice.questionBank)

  const typeLabels: Record<string, string> = {
    translation: '中英名词互译',
    'true-false': '判断题',
    'multiple-choice': '选择题',
    'short-answer': '简答题',
    essay: '分析论述题',
  }

  return (
    <div className="page-stack">
      {/* Hero */}
      <section className="panel hero-panel hero-grid">
        <div className="hero-copy">
          <h1>分子生物学习题库</h1>
          <p className="lead">
            覆盖名词互译、判断、选择、简答、论述五大题型。支持按题型自由组卷、自主判分与错题回顾。
          </p>
          <div className="cta-row">
            <Link to="/categories" className="primary-button">
              开始练习
            </Link>
            {practice.session && (
              <Link to="/practice" className="secondary-button">
                继续上次练习
              </Link>
            )}
            {practice.mistakeRecords.length > 0 && (
              <Link to="/mistakes" className="ghost-button">
                错题本（{practice.mistakeRecords.length}）
              </Link>
            )}
          </div>
        </div>

        <div className="metric-grid" style={{ flex: '0 0 320px' }}>
          <div className="metric-card">
            <strong>{practice.questionBank.totalQuestions}</strong>
            <span>总题量</span>
          </div>
          <div className="metric-card">
            <strong>{types.length}</strong>
            <span>题型类别</span>
          </div>
          <div className="metric-card">
            <strong>{practice.questionBank.categories.length}</strong>
            <span>子分类</span>
          </div>
          <div className="metric-card">
            <strong>{practice.mistakeRecords.length}</strong>
            <span>待复习错题</span>
          </div>
        </div>
      </section>

      {/* Feature cards */}
      <section className="feature-grid">
        {types.map((type) => {
          const label = typeLabels[type] || type
          const cats = practice.questionBank.categories.filter((c) => c.type === type)
          const count = cats.reduce((sum, c) => sum + c.questionCount, 0)
          return (
            <div key={type} className="panel feature-card">
              <h2>{label}</h2>
              <p>{count} 道题，{cats.length} 个子分类</p>
              <p className="panel-note">
                {type === 'translation' && '支持缩写匹配，仅答缩写即判对'}
                {type === 'true-false' && '判断正误，即时反馈解析'}
                {type === 'multiple-choice' && '四选一，含AI生成解析'}
                {type === 'short-answer' && '自主作答后揭晓答案，自己判分'}
                {type === 'essay' && '论述分析，揭晓答案后自主判分'}
              </p>
            </div>
          )
        })}
      </section>

      {/* Usage guide */}
      <section className="panel compact-panel">
        <h2 style={{ marginBottom: 16 }}>使用指南</h2>
        <div className="timeline-grid">
          <div className="timeline-step">
            <strong>1. 选择题型</strong>
            <p>在题型选择页勾选想要练习的题型和子分类</p>
          </div>
          <div className="timeline-step">
            <strong>2. 答题练习</strong>
            <p>按题型依次作答：输入翻译、判断正误、选择题选项、简答自主判分</p>
          </div>
          <div className="timeline-step">
            <strong>3. 查看结果</strong>
            <p>完成练习后查看成绩统计，区分自动判分与自主判分</p>
          </div>
          <div className="timeline-step">
            <strong>4. 错题回顾</strong>
            <p>错题自动收入错题本，支持错题专项练习</p>
          </div>
        </div>
      </section>
    </div>
  )
}
