import { createClient } from '@supabase/supabase-js'

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end()

  const { result, questionsAnswered } = req.body
  const ip = (req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'unknown')
    .split(',')[0].trim()

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  )

  const today = new Date().toISOString().slice(0, 10)

  const { error } = await supabase
    .from('game_plays')
    .upsert(
      { ip, play_date: today, result, questions_answered: questionsAnswered },
      { onConflict: 'ip,play_date' }
    )

  if (error) console.error('record-result supabase error:', error)

  return res.status(200).json({ ok: true })
}
