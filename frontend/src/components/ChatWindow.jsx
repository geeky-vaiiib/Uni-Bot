import { useEffect, useRef } from 'react'
import './ChatWindow.css'

function ChatWindow({ messages, isLoading }) {
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages, isLoading])

    const formatTime = (date) => {
        return new Date(date).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    const getConfidenceLabel = (confidence) => {
        switch (confidence) {
            case 'verified':
                return { icon: '✓', text: 'Verified from official documents' }
            case 'partial':
                return { icon: '◐', text: 'Partial match found' }
            case 'not_found':
                return { icon: '✗', text: 'Information not found' }
            default:
                return { icon: '•', text: confidence }
        }
    }

    return (
        <div className="chat-window">
            {messages.map((message) => (
                <div
                    key={message.id}
                    className={`message ${message.type} ${message.isError ? 'error' : ''}`}
                >
                    <div className="message-avatar">
                        {message.type === 'user' ? '👤' : '🎓'}
                    </div>

                    <div className="message-bubble">
                        <div className="message-content">
                            {message.content}
                        </div>

                        {/* Sources section for bot messages */}
                        {message.type === 'bot' && message.sources && message.sources.length > 0 && (
                            <div className="message-sources">
                                <div className="sources-title">
                                    <span>📄</span> Sources
                                </div>
                                {message.sources.map((source, idx) => (
                                    <div key={idx} className="source-item">
                                        <span className="source-icon">•</span>
                                        <div>
                                            <div className="source-name">{source.source}</div>
                                            {source.section && (
                                                <div className="source-section">{source.section}</div>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Confidence badge */}
                        {message.type === 'bot' && message.confidence && !message.isError && (
                            <div className={`confidence-badge ${message.confidence}`}>
                                <span>{getConfidenceLabel(message.confidence).icon}</span>
                                {getConfidenceLabel(message.confidence).text}
                            </div>
                        )}

                        <div className="message-time">
                            {formatTime(message.timestamp)}
                        </div>
                    </div>
                </div>
            ))}

            {/* Loading indicator */}
            {isLoading && (
                <div className="loading-message">
                    <div className="message-avatar">🎓</div>
                    <div className="loading-bubble">
                        <div className="loading-dots">
                            <div className="loading-dot"></div>
                            <div className="loading-dot"></div>
                            <div className="loading-dot"></div>
                        </div>
                    </div>
                </div>
            )}

            <div ref={messagesEndRef} />
        </div>
    )
}

export default ChatWindow
