import type { TrueFalseQuestion } from '../types'
import type { PracticeAnswer, AnswerSelection } from '../types'
import { useLanguage } from '../context/LanguageContext'
import { useT } from '../lib/i18n'

interface TrueFalseInputProps {
  question: TrueFalseQuestion
  existingAnswer: PracticeAnswer | undefined
  onAnswer: (questionId: string, selectedKey: AnswerSelection) => void
}

export function TrueFalseInput({
  question,
  existingAnswer,
  onAnswer,
}: TrueFalseInputProps) {
  const { language } = useLanguage()
  const t = useT()
  const answered = Boolean(existingAnswer)
  const isCorrect = existingAnswer?.isCorrect ?? false
  const userChoice = existingAnswer?.selectedKey

  const prompt = language === 'zh' ? (question.promptCn ?? question.prompt) : question.prompt
  const explanation = language === 'zh' ? (question.explanationCn ?? question.explanation) : question.explanation

  function handleSelect(choice: AnswerSelection) {
    if (answered) return
    onAnswer(question.id, choice)
  }

  function getButtonClass(buttonKey: string) {
    if (!answered) return 'option-button'

    const isThisCorrect = (buttonKey === 'A') === question.answerIsTrue
    const isThisSelected = userChoice === buttonKey

    if (isThisCorrect) return 'option-button is-correct'
    if (isThisSelected && !isCorrect) return 'option-button is-incorrect'
    return 'option-button is-muted'
  }

  return (
    <div className="question-panel">
      <p className="question-text">{prompt}</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
        <button
          className={getButtonClass('A')}
          onClick={() => handleSelect('A')}
          disabled={answered}
          style={{ justifyContent: 'center', textAlign: 'center' }}
        >
          <strong>{t('tf', 'correct')}</strong>
        </button>

        <button
          className={getButtonClass('B')}
          onClick={() => handleSelect('B')}
          disabled={answered}
          style={{ justifyContent: 'center', textAlign: 'center' }}
        >
          <strong>{t('tf', 'incorrect')}</strong>
        </button>
      </div>

      {answered && (
        <div className={`answer-banner ${isCorrect ? 'is-visible' : ''}`}>
          {isCorrect ? (
            <strong style={{ color: 'var(--correct)' }}>{t('tf', 'correctMsg')}</strong>
          ) : (
            <strong style={{ color: 'var(--incorrect)' }}>
              {t('tf', 'wrongMsg')}{question.answerIsTrue ? t('tf', 'correct') : t('tf', 'incorrect')}
            </strong>
          )}
          {explanation && (
            <div className="explanation-panel" style={{ marginTop: 12 }}>
              <strong>{t('tf', 'explanation')}</strong>
              <p>{explanation}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
