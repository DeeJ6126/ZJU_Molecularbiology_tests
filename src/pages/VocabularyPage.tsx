import { useRef, useState } from 'react'
import { usePractice } from '../hooks/usePractice'
import { useT } from '../lib/i18n'
import type { VocabularyRecord, VocabularyStatus } from '../types'

export function VocabularyPage() {
  const practice = usePractice()
  const t = useT()
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
        alert(t('vocab', 'importError'))
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
            <h2>{t('vocab', 'title')}</h2>
            <p className="scope-note">
              {t('vocab', 'subtitle').replace('{n}', String(vocabularyRecords.length))}
            </p>
          </div>
          <div className="toolbar-actions">
            <button className="ghost-button file-button" style={{ position: 'relative', overflow: 'hidden' }}>
              {t('vocab', 'import')}
              <input
                ref={fileInputRef}
                type="file"
                accept=".json"
                onChange={handleImport}
              />
            </button>
            <button className="ghost-button" onClick={handleExport}>
              {t('vocab', 'export')}
            </button>
            <button className="ghost-button" onClick={clearVocabularyRecords}>
              {t('vocab', 'clear')}
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
              {status === 'all' ? t('vocab', 'all') : t('vocab.statusLabels', status)}
            </button>
          ))}
        </div>
      </section>

      {!filtered.length ? (
        <section className="panel empty-state">
          <h2>{t('vocab', 'emptyTitle')}</h2>
          <p>{t('vocab', 'emptyDesc')}</p>
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
                  {t('vocab', 'delete')}
                </button>
              </div>
              <p className="vocabulary-context">{record.contextText}</p>
              <div className="vocabulary-meta">
                <span className={`vocabulary-status status-${record.status}`}>
                  {t('vocab.statusLabels', record.status)}
                </span>
                <button
                  className="secondary-button"
                  onClick={() => handleStatusChange(record.id, record.status)}
                >
                  {t('vocab.nextStatus', record.status)}
                </button>
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  )
}

