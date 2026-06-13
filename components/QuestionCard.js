import { useState } from 'react'

export default function QuestionCard({ playerName, question, questionNumber, total, onSubmit, isJudging, feedback }) {
  const [answer, setAnswer] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    const trimmed = answer.trim()
    if (!trimmed || isJudging) return
    onSubmit(trimmed)
    setAnswer('')
  }

  const dots = Array.from({ length: total }, (_, i) => {
    if (i < questionNumber - 1) return 'answered'
    if (i === questionNumber - 1) return 'current'
    return ''
  })

  return (
    <div className="card">
      <div className="progress-dots">
        {dots.map((state, i) => (
          <div key={i} className={`dot ${state}`} title={`Question ${i + 1}`} />
        ))}
      </div>

      <p className="question-label">{playerName}, question {questionNumber} of {total}</p>
      <h2>{question.text}</h2>

      {isJudging ? (
        <div>
          <div className="spinner" />
          <p style={{ color: '#666', fontSize: '0.9rem' }}>The tree listens...</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <textarea
            value={answer}
            onChange={e => setAnswer(e.target.value)}
            placeholder="Share your truth here..."
            disabled={isJudging}
            autoFocus
          />
          <br />
          <button className="btn btn-primary" type="submit" disabled={!answer.trim()}>
            Offer your answer
          </button>
        </form>
      )}

      {feedback && !isJudging && (
        <div className={`feedback-banner ${feedback.pass ? 'feedback-pass' : 'feedback-fail'}`}>
          {feedback.text}
        </div>
      )}
    </div>
  )
}
