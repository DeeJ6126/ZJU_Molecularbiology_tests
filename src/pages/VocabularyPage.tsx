import { useRef, useState } from 'react'
import { usePractice } from '../hooks/usePractice'
import type { VocabularyRecord, VocabularyStatus } from '../types'

const STATUS_LABELS: Record<VocabularyStatus, string> = {
  new: '新词',
  learning: '学习中',
  mastered: '已掌握',
}

export function VocabularyPage() {
  const practice = usePractice()
  const { vocabularyRecords, removeVocabularyRecord, updateVocabularyRecordStatus, importVocabularyRecords, clearVocabularyRecords } = practice
  const fileInputRef = useRef<HTMLInputElement>(null)

  const [statusFilter, setStatusFilter] = useState<VocabularyStatus | 'all'>('all')

  const filtered =
    statusFilter === 'all'
      ? vocabularyRecords
      : vocabularyRecords.filter((r) => r.status === statusFilter)

  function handleStatusChange(recordId: string, currentStatus: VocabularyStatus) {
    const next: VocabularyStatus =
      currentStatus === 'new'
        ? 'learning'
        : currentStatus === 'learning'
          ? 'mastered'
          : 'new'
    updateVocabularyRecordStatus(recordId, next)
  }

  function handleExport() {
    const blob = new Blob([JSON.stringify(vocabularyRecords, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `molecular-biology-vocabulary-${new Date().toISOString().slice(0, 10)}.json`
    anchor.click()
    URL.revokeObjectURL(url)
  }

  function handleImport(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = () => {
      try {
        const records = JSON.parse(reader.result as string) as VocabularyRecord[]
        importVocabularyRecords(records)
      } catch {
        alert('文件格式不正确')
      }
    }
    reader.readAsText(file)

    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="page-stack">
      <section className="panel compact-panel">
        <div className="section-heading">
          <div>
            <h2>生词本</h2>
            <p className="scope-note">
              练习中通过取词模式收集的英文术语，共 <strong>{vocabularyRecords.length}</strong> 个。
            </p>
          </div>
          <div className="toolbar-actions">
            <button className="ghost-button file-button" style={{ position: 'relative', overflow: 'hidden' }}>
              导入
              <input
                ref={fileInputRef}
                type="file"
                accept=".json"
                onChange={handleImport}
              />
            </button>
            <button className="ghost-button" onClick={handleExport}>
              导出
            </button>
            <button className="ghost-button" onClick={clearVocabularyRecords}>
              清空
            </button>
          </div>
        </div>
        <div className="toolbar-actions" style={{ marginTop: 14 }}>
          {(['all', 'new', 'learning', 'mastered'] as const).map((status) => (
            <button
              key={status}
              className={`secondary-button ${statusFilter === status ? 'is-active' : ''}`}
              onClick={() => setStatusFilter(status)}
            >
              {status === 'all' ? '全部' : STATUS_LABELS[status]}
            </button>
          ))}
        </div>
      </section>

      {!filtered.length ? (
        <section className="panel empty-state">
          <h2>暂无生词</h2>
          <p>在练习页开启取词模式，点击题目中的英文术语即可添加到生词本。</p>
        </section>
      ) : (
        <div className="vocabulary-grid">
          {filtered.map((record) => (
            <section key={record.id} className="panel vocabulary-card">
              <div className="vocabulary-card-top">
                <h2>{record.term}</h2>
                <button
                  className="ghost-button"
                  onClick={() => removeVocabularyRecord(record.id)}
                >
                  删除
                </button>
              </div>
              <p className="vocabulary-context">{record.contextText}</p>
              <div className="vocabulary-meta">
                <span className={`vocabulary-status status-${record.status}`}>
                  {STATUS_LABELS[record.status]}
                </span>
                <button
                  className="secondary-button"
                  onClick={() => handleStatusChange(record.id, record.status)}
                >
                  {record.status === 'new'
                    ? '→ 学习中'
                    : record.status === 'learning'
                      ? '→ 已掌握'
                      : '→ 新词'}
                </button>
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  )
}

