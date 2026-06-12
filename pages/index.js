import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import Tree from '../components/Tree'
import Fence from '../components/Fence'
import NameEntry from '../components/NameEntry'
import QuestionCard from '../components/QuestionCard'
import AlreadyPlayed from '../components/AlreadyPlayed'

const ResultCard = dynamic(() => import('../components/ResultCard'), { ssr: false })

const QUESTIONS = [
  {
    text: 'Describe a moment that changed the way you see the world.',
    criteria: 'The answer must show genuine reflection and personal growth, not just a surface-level event.',
  },
  {
    text: 'What would you sacrifice to protect something you truly love?',
    criteria: 'The answer must demonstrate depth of values and go beyond material or trivial things.',
  },
  {
    text: 'If you could only keep one memory forever, what would it be and why?',
    criteria: 'The answer must be specific and carry emotional meaning, not a vague or generic response.',
  },
  {
    text: 'What does true success look like for you in 10 years?',
    criteria: 'The answer must go beyond money, status, or possessions — it must reflect personal meaning.',
  },
  {
    text: 'Describe a time you were wrong about something important and what it cost you.',
    criteria: 'The answer must show genuine accountability and self-awareness, not deflection.',
  },
  {
    text: 'What is something most people misunderstand about who you really are?',
    criteria: 'The answer must be honest and self-aware, not a performance.',
  },
  {
    text: 'Why are you here, walking this path today?',
    criteria: 'Any sincere, thoughtful answer passes. Only dismissive or empty answers fail.',
  },
]

const STATES = {
  LOADING:        'LOADING',
  ALREADY_PLAYED: 'ALREADY_PLAYED',
  INTRO:          'INTRO',
  NAME_ENTRY:     'NAME_ENTRY',
  QUESTION:       'QUESTION',
  JUDGING:        'JUDGING',
  GROWING:        'GROWING',
  DYING:          'DYING',
  GAME_OVER:      'GAME_OVER',
  WIN:            'WIN',
}

export default function Home() {
  const [gameState,        setGameState]        = useState(STATES.LOADING)
  const [playerName,       setPlayerName]       = useState('')
  const [currentQ,         setCurrentQ]         = useState(0)   // 0-indexed
  const [treeStage,        setTreeStage]        = useState(0)
  const [isDying,          setIsDying]          = useState(false)
  const [isWon,            setIsWon]            = useState(false)
  const [feedback,         setFeedback]         = useState(null)
  const [alreadyPlayedData,setAlreadyPlayedData]= useState(null)

  // Check IP on mount
  useEffect(() => {
    fetch('/api/check-play')
      .then(r => r.json())
      .then(data => {
        if (data.played) {
          setAlreadyPlayedData(data)
          setGameState(STATES.ALREADY_PLAYED)
        } else {
          setGameState(STATES.INTRO)
        }
      })
      .catch(() => setGameState(STATES.INTRO))
  }, [])

  function handleStart() {
    setGameState(STATES.NAME_ENTRY)
  }

  function handleNameSubmit(name) {
    setPlayerName(name)
    setGameState(STATES.QUESTION)
  }

  async function handleAnswerSubmit(answer) {
    setFeedback(null)
    setGameState(STATES.JUDGING)

    const q = QUESTIONS[currentQ]
    let result
    try {
      const resp = await fetch('/api/judge-answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q.text, criteria: q.criteria, answer }),
      })
      result = await resp.json()
    } catch {
      result = { pass: false, feedback: 'The tree could not hear your answer.' }
    }

    setFeedback({ pass: result.pass, text: result.feedback })

    if (result.pass) {
      const nextStage = treeStage + 1
      setTreeStage(nextStage)

      await pause(1400)
      setFeedback(null)

      if (currentQ + 1 >= QUESTIONS.length) {
        // Won!
        setIsWon(true)
        setGameState(STATES.WIN)
        await recordResult('win', QUESTIONS.length)
      } else {
        setCurrentQ(q => q + 1)
        setGameState(STATES.QUESTION)
      }
    } else {
      // Wrong — die
      await pause(1200)
      setFeedback(null)
      setIsDying(true)
      setGameState(STATES.DYING)
      await recordResult('lose', currentQ + 1)
      await pause(3200)
      setGameState(STATES.GAME_OVER)
    }
  }

  async function recordResult(result, questionsAnswered) {
    try {
      await fetch('/api/record-result', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ result, questionsAnswered }),
      })
    } catch { /* silent */ }
  }

  function handlePlayAgain() {
    // Reset all state — IP block will prevent actual replay until tomorrow
    setGameState(STATES.ALREADY_PLAYED)
    setAlreadyPlayedData({
      result: isWon ? 'win' : 'lose',
      questionsAnswered: isWon ? QUESTIONS.length : currentQ + 1,
    })
  }

  const showCard = [STATES.INTRO, STATES.NAME_ENTRY, STATES.QUESTION, STATES.JUDGING, STATES.GAME_OVER, STATES.WIN, STATES.ALREADY_PLAYED].includes(gameState)

  return (
    <div className="scene">
      {/* Sky */}
      <div className="sky" />

      {/* Clouds */}
      <div className="clouds">
        <div className="cloud cloud-1" />
        <div className="cloud cloud-2" />
        <div className="cloud cloud-3" />
      </div>

      {/* Sun */}
      <div className="sun" />

      {/* Tree */}
      <div className="tree-container">
        <Tree stage={treeStage} dying={isDying} won={isWon} />
      </div>

      {/* Ground */}
      <div className="ground" />

      {/* Fence */}
      <div className="fence">
        <Fence />
      </div>

      {/* UI Overlay */}
      {showCard && (
        <div className="ui-overlay">
          {gameState === STATES.LOADING && (
            <div className="card"><div className="spinner" /></div>
          )}

          {gameState === STATES.ALREADY_PLAYED && alreadyPlayedData && (
            <AlreadyPlayed
              result={alreadyPlayedData.result}
              questionsAnswered={alreadyPlayedData.questionsAnswered}
              total={QUESTIONS.length}
            />
          )}

          {gameState === STATES.INTRO && (
            <div className="card">
              <h1>The Tree of Life</h1>
              <p>
                Within its branches lie answers waiting to be found.<br/>
                Today, it grows for those who seek — or withers for those who do not.<br/><br/>
                Seven questions stand between a seed and full bloom.<br/>
                Answer them with honesty. The tree knows.
              </p>
              <p style={{ fontSize: '0.9rem', color: '#888' }}>One chance per day. Choose your words carefully.</p>
              <button className="btn btn-primary" onClick={handleStart}>
                Begin your journey
              </button>
            </div>
          )}

          {gameState === STATES.NAME_ENTRY && (
            <NameEntry onSubmit={handleNameSubmit} />
          )}

          {(gameState === STATES.QUESTION || gameState === STATES.JUDGING) && (
            <QuestionCard
              playerName={playerName}
              question={QUESTIONS[currentQ]}
              questionNumber={currentQ + 1}
              total={QUESTIONS.length}
              onSubmit={handleAnswerSubmit}
              isJudging={gameState === STATES.JUDGING}
              feedback={feedback}
            />
          )}

          {gameState === STATES.DYING && (
            <div className="card">
              <h2>The tree feels your doubt...</h2>
              <p>Its leaves tremble. The branches weaken.</p>
              {feedback && (
                <div className="feedback-banner feedback-fail">{feedback.text}</div>
              )}
            </div>
          )}

          {gameState === STATES.GAME_OVER && (
            <ResultCard
              won={false}
              playerName={playerName}
              questionsAnswered={currentQ + 1}
              total={QUESTIONS.length}
              onPlayAgain={handlePlayAgain}
            />
          )}

          {gameState === STATES.WIN && (
            <ResultCard
              won={true}
              playerName={playerName}
              questionsAnswered={QUESTIONS.length}
              total={QUESTIONS.length}
              onPlayAgain={handlePlayAgain}
            />
          )}
        </div>
      )}
    </div>
  )
}

function pause(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}
