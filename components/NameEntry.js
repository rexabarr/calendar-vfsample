import { useState } from 'react'

export default function NameEntry({ onSubmit }) {
  const [name, setName] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    const trimmed = name.trim()
    if (!trimmed) return
    onSubmit(trimmed)
  }

  return (
    <div className="card">
      <h2>Before we begin...</h2>
      <p>The tree wishes to know your name, traveller.</p>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Enter your name"
          maxLength={40}
          autoFocus
        />
        <br />
        <button className="btn btn-primary" type="submit" disabled={!name.trim()}>
          Step forward
        </button>
      </form>
    </div>
  )
}
