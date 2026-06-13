const WEBHOOK_URL = 'https://hook.us1.make.com/kjn9f9q1c9hqwrjw6fkd1vmy8zy7e9h8'

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end()

  try {
    await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body),
    })
    return res.status(200).json({ ok: true })
  } catch (err) {
    console.error('submit-webhook error:', err)
    return res.status(500).json({ ok: false })
  }
}
