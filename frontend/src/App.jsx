import React, { useState } from 'react'

export default function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [processed, setProcessed] = useState([])

  async function handleSubmit(e) {
    e.preventDefault()
    if (!file) return setError('Select a file first')
    setError(null)
    setLoading(true)
    try {
      const fd = new FormData()
      fd.append('file', file)
      const res = await fetch('/process-text', { method: 'POST', body: fd })
      if (!res.ok) throw new Error(`Server responded ${res.status}`)
      const data = await res.json()
      setProcessed(data.processed_words || data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function renderAnnotated(tokens) {
    if (!tokens || tokens.length === 0) return null
    const nodes = []
    tokens.forEach((t, i) => {
      const w = t.word
      const isPunct = /^[.,!?;]$/.test(w)
      // add space if needed
      if (i > 0) {
        const prev = tokens[i - 1].word
        if (!/^[.,!?;]$/.test(prev) && !isPunct) nodes.push(' ')
        if (!/^[.,!?;]$/.test(prev) && isPunct) nodes.push('')
        if (/^[.,!?;]$/.test(prev) && !isPunct) nodes.push(' ')
      }
      if (t.is_hard) {
        nodes.push(
          <span key={i} className="hard" title={t.definition || 'No definition'}>
            {w}
          </span>
        )
      } else {
        nodes.push(
          <span key={i} className="token">
            {w}
          </span>
        )
      }
    })
    return nodes
  }

  return (
    <div className="container">
      <h1>Reading Helper — Frontend</h1>
      <form onSubmit={handleSubmit} className="upload-form">
        <input
          type="file"
          accept=".txt"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Process'}
        </button>
      </form>
      {error && <div className="error">{error}</div>}

      <section className="results">
        <h2>Annotated Text</h2>
        <div className="annotated">
          {processed.length === 0 ? (
            <p>No results yet. Upload a plain text file.</p>
          ) : (
            <div className="text">{renderAnnotated(processed)}</div>
          )}
        </div>

        {processed.length > 0 && (
          <div className="definitions">
            <h3>Definitions</h3>
            <ul>
              {processed
                .filter((t) => t.is_hard)
                .map((t, i) => (
                  <li key={i}>
                    <strong>{t.word}</strong>: {t.definition || '—'}
                  </li>
                ))}
            </ul>
          </div>
        )}
      </section>
    </div>
  )
}
