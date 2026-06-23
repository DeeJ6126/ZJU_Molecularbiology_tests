export function AboutPage() {
  return (
    <div className="page-stack">
      <section className="panel hero-panel">
        <h1>关于本应用</h1>
        <p className="lead" style={{ marginTop: 16 }}>
          分子生物学习题库 — 浙江大学分子生物学课程复习工具
        </p>
      </section>

      <section className="panel compact-panel">
        <h2 style={{ marginBottom: 16 }}>内容说明</h2>
        <div className="about-list" style={{ gap: 12 }}>
          <div className="about-row">
            <strong>题库来源</strong>
            <span>历年考试真题汇总，按题型分类整理</span>
          </div>
          <div className="about-row">
            <strong>五大题型</strong>
            <span>中英名词互译、判断题、选择题、简答题、分析论述题</span>
          </div>
          <div className="about-row">
            <strong>缩写匹配</strong>
            <span>中英互译题支持仅答缩写（如 ChIP）即判对</span>
          </div>
          <div className="about-row">
            <strong>自主判分</strong>
            <span>简答题与论述题不自动判分，由你对照参考答案自行判断</span>
          </div>
          <div className="about-row">
            <strong>错题本</strong>
            <span>答错的题目自动收入错题本，支持错题专项练习</span>
          </div>
          <div className="about-row">
            <strong>生词本</strong>
            <span>开启取词模式后可点击题目中英文术语收入生词本</span>
          </div>
        </div>
      </section>

      <section className="panel compact-panel">
        <h2 style={{ marginBottom: 16 }}>技术实现</h2>
        <p className="panel-note">
          React 19 + Vite 8 + TypeScript 6，纯静态前端应用。
          所有练习数据仅存储在浏览器本地（localStorage），不上传任何服务器。
        </p>
      </section>
    </div>
  )
}
