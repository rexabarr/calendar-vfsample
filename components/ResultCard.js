import { useRef } from 'react'

export default function ResultCard({ won, playerName, questionsAnswered, total, onPlayAgain }) {
  const captureRef = useRef(null)

  async function handleShare() {
    if (typeof window === 'undefined') return
    try {
      const html2canvas = (await import('html2canvas')).default
      const canvas = await html2canvas(captureRef.current, { useCORS: true, scale: 2 })
      canvas.toBlob(blob => {
        if (!blob) return
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `tree-of-life-${won ? 'victory' : 'fallen'}.png`
        a.click()
        URL.revokeObjectURL(url)
      }, 'image/png')
    } catch {
      alert('Could not capture image. Try a screenshot!')
    }
  }

  const today = new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })

  return (
    <div className={`card ${won ? 'win-glow' : ''}`}>
      <div ref={captureRef} className={`result-capture ${won ? '' : 'lose-card'}`}>
        <div className="result-title">
          {won
            ? `The Tree bloomed for ${playerName}!`
            : `The Tree has fallen, ${playerName}.`}
        </div>
        <div className="result-score">
          {won
            ? `All ${total} questions answered. Full bloom achieved.`
            : `Reached question ${questionsAnswered} of ${total}.`}
        </div>
        <div style={{ fontSize: '0.82rem', color: '#888', marginTop: 6 }}>{today} · Tree of Life</div>
      </div>

      <p style={{ marginBottom: 8 }}>
        {won
          ? 'You have walked the full path. The tree stands in full bloom, a testament to your truth.'
          : 'The tree has withered. Return tomorrow when you are ready to seek again.'}
      </p>

      <button className="btn btn-share" onClick={handleShare}>
        Save result card
      </button>
      <button className="btn btn-secondary" onClick={onPlayAgain} style={{ marginLeft: 10 }}>
        {won ? 'Play again tomorrow' : 'Try again tomorrow'}
      </button>
    </div>
  )
}
