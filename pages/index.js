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
    text: 'What first made you fall for your spouse, and when did you last make them feel that way?',
    criteria: 'Must include a sincere specific memory and some honest reflection on whether they have shown up that way recently. Vague or deflecting answers fail.',
  },
  {
    text: 'Name three things you know you could be doing better but have not been.',
    criteria: 'Must name at least three specific areas. Health, financial contribution, or relationship effort should be present. Vague answers like "everything" or "I don\'t know" fail.',
  },
  {
    text: "What is your plan to get healthier or back in shape? What will you actually do, and by when?",
    criteria: 'Must name a concrete action (for example: exercise type, diet change) and give a realistic timeframe. Answers like "I will try" or "eventually" fail.',
  },
  {
    text: 'Are you willing to bring in income to take pressure off the household? If so, what kind of work, and by when?',
    criteria: 'Must show genuine willingness and name a realistic type of work with a timeframe. Deflection or vague "maybe someday" answers fail.',
  },
  {
    text: 'Describe one way you have been hard to live with lately, and how you will show up kinder this week.',
    criteria: 'Must show real self-awareness about a specific behavior, plus a concrete plan to improve this week. Vague promises or blaming others fails.',
  },
  {
    text: 'Why does becoming this better version of yourself matter to you right now?',
    criteria: 'Any sincere, personal answer passes. Only dismissive, sarcastic, or empty answers fail.',
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
  const [treeStage,        setTreeStage]        = useState(1)
  const [answers,          setAnswers]          = useState([])
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
    const newAnswers = [...answers, { question: q.text, answer }]
    setAnswers(newAnswers)

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
        setIsWon(true)
        setGameState(STATES.WIN)
        await recordResult('win', QUESTIONS.length)
        await sendWebhook(newAnswers, 'win')
      } else {
        setCurrentQ(q => q + 1)
        setGameState(STATES.QUESTION)
      }
    } else {
      await pause(1200)
      setFeedback(null)
      setIsDying(true)
      setGameState(STATES.DYING)
      await recordResult('lose', currentQ + 1)
      await sendWebhook(newAnswers, 'lose')
      await pause(3200)
      setGameState(STATES.GAME_OVER)
    }
  }

  async function sendWebhook(allAnswers, result) {
    try {
      await fetch('/api/submit-webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          playerName,
          result,
          date: new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }),
          answers: allAnswers,
        }),
      })
    } catch { /* silent */ }
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
                Today, it grows for those who seek, or withers for those who do not.<br/><br/>
                Six questions stand between a seed and full bloom.<br/>
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
