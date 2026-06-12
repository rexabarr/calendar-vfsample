import Anthropic from '@anthropic-ai/sdk'

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end()

  const { question, criteria, answer } = req.body

  if (!question || !criteria || !answer) {
    return res.status(400).json({ error: 'Missing fields' })
  }

  const prompt = `You are a wise, fair judge for a reflective game called "Tree of Life".
Your role: decide if the player's answer meets the creator's criteria. Be thoughtful but not overly strict — genuine effort and sincerity count.

Question: ${question}
Creator's criteria: ${criteria}
Player's answer: ${answer}

Respond ONLY with valid JSON (no markdown, no extra text):
{"pass": true or false, "feedback": "one short, poetic sentence about their answer (max 20 words)"}`

  try {
    const message = await client.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 120,
      messages: [{ role: 'user', content: prompt }],
    })

    const raw = message.content[0].text.trim()
    const parsed = JSON.parse(raw)

    return res.status(200).json({
      pass: Boolean(parsed.pass),
      feedback: String(parsed.feedback || ''),
    })
  } catch (err) {
    console.error('judge-answer error:', err)
    return res.status(500).json({ error: 'Judgment failed', pass: false, feedback: 'The tree could not hear your words.' })
  }
}
