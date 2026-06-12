export default function AlreadyPlayed({ result, questionsAnswered, total }) {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  const tomorrowStr = tomorrow.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })

  return (
    <div className="card">
      <div className="already-played-icon">{result === 'win' ? '🌳' : '🍂'}</div>
      <h2>You have already visited the tree today.</h2>
      <p>
        {result === 'win'
          ? `You answered all ${total} questions and the tree bloomed fully. Come back tomorrow to walk the path again.`
          : `The tree fell at question ${questionsAnswered}. It needs time to recover. Return on ${tomorrowStr}.`}
      </p>
      <p style={{ fontSize: '0.9rem', color: '#888' }}>The tree rests until {tomorrowStr}.</p>
    </div>
  )
}
