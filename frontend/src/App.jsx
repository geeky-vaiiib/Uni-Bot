import { useState, useEffect } from 'react'
import Header from './components/Header'
import ChatWindow from './components/ChatWindow'
import InputArea from './components/InputArea'
import ModeSelector from './components/ModeSelector'
import WelcomeScreen from './components/WelcomeScreen'
import QuickSuggestions from './components/QuickSuggestions'
import './App.css'

const API_BASE = 'http://localhost:8000'

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [mode, setMode] = useState('student')
  const [theme, setTheme] = useState('light')
  const [hasStarted, setHasStarted] = useState(false)

  // Apply theme to document
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  const handleSendMessage = async (question) => {
    if (!question.trim() || isLoading) return

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: question,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setHasStarted(true)

    try {
      const response = await fetch(`${API_BASE}/api/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          mode: mode
        })
      })

      if (!response.ok) {
        throw new Error('Failed to get response')
      }

      const data = await response.json()

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: data.answer,
        sources: data.sources || [],
        confidence: data.confidence,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, botMessage])

    } catch (error) {
      console.error('Error:', error)
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'I apologize, but I encountered an error while processing your request. Please ensure the backend server is running and try again.',
        isError: true,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleQuickQuestion = (question) => {
    handleSendMessage(question)
  }

  const clearChat = () => {
    setMessages([])
    setHasStarted(false)
  }

  return (
    <div className="app">
      <Header
        theme={theme}
        onToggleTheme={toggleTheme}
        onClearChat={clearChat}
        hasMessages={messages.length > 0}
      />

      <main className="main-container">
        <div className="chat-container">
          {!hasStarted ? (
            <WelcomeScreen onQuickQuestion={handleQuickQuestion} />
          ) : (
            <ChatWindow
              messages={messages}
              isLoading={isLoading}
            />
          )}

          <div className="input-section">
            {hasStarted && (
              <QuickSuggestions onSelect={handleQuickQuestion} />
            )}
            <ModeSelector mode={mode} onModeChange={setMode} />
            <InputArea
              onSend={handleSendMessage}
              isLoading={isLoading}
              placeholder={`Ask about SIT academics, admissions, policies...`}
            />
          </div>
        </div>
      </main>
    </div>
  )
}

export default App

