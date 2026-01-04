import { useState, useRef, useEffect } from 'react'
import './InputArea.css'

const MAX_CHARS = 1000

function InputArea({ onSend, isLoading, placeholder }) {
    const [input, setInput] = useState('')
    const textareaRef = useRef(null)

    // Auto-resize textarea
    useEffect(() => {
        const textarea = textareaRef.current
        if (textarea) {
            textarea.style.height = 'auto'
            textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px'
        }
    }, [input])

    const handleSubmit = (e) => {
        e?.preventDefault()
        if (input.trim() && !isLoading && input.length <= MAX_CHARS) {
            onSend(input.trim())
            setInput('')
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSubmit()
        }
    }

    const charCount = input.length
    const charCountClass = charCount > MAX_CHARS ? 'error' : charCount > MAX_CHARS * 0.9 ? 'warning' : ''

    return (
        <form className="input-area" onSubmit={handleSubmit}>
            <div className="input-wrapper">
                <textarea
                    ref={textareaRef}
                    className="input-field"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder={placeholder || "Ask a question about SIT..."}
                    disabled={isLoading}
                    rows={1}
                    aria-label="Question input"
                />
                {charCount > 0 && (
                    <span className={`char-count ${charCountClass}`}>
                        {charCount}/{MAX_CHARS}
                    </span>
                )}
            </div>

            <button
                type="submit"
                className={`send-btn ${isLoading ? 'loading' : ''}`}
                disabled={!input.trim() || isLoading || charCount > MAX_CHARS}
                aria-label="Send message"
            >
                <span className="send-icon">
                    {isLoading ? '⏳' : '→'}
                </span>
            </button>
        </form>
    )
}

export default InputArea
