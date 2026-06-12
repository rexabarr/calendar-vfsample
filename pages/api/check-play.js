import { createClient } from '@supabase/supabase-js'

export default async function handler(req, res) {
  if (req.method !== 'GET') return res.status(405).end()

  const ip = (req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'unknown')
    .split(',')[0].trim()

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  )

  const today = new Date().toISOString().slice(0, 10)

  const { data, error } = await supabase
    .from('game_plays')
    .select('result, questions_answered')
    .eq('ip', ip)
    .eq('play_date', today)
    .maybeSingle()

  if (error) {
    console.error('check-play supabase error:', error)
    // On DB error, allow play rather than blocking everyone
    return res.status(200).json({ played: false })
  }

  if (data) {
    return res.status(200).json({
      played: true,
      result: data.result,
      questionsAnswered: data.questions_answered,
    })
  }

  return res.status(200).json({ played: false })
}
