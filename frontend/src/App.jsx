import { useState, useEffect } from 'react'
import Header from './components/Header'
import ChatWindow from './components/ChatWindow'
import InputArea from './components/InputArea'
import ModeSelector from './components/ModeSelector'
import WelcomeScreen from './components/WelcomeScreen'
import QuickSuggestions from './components/QuickSuggestions'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import './App.css'

const API_BASE = 'http://localhost:8000'

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [mode, setMode] = useState('student')
  const [theme, setTheme] = useState('dark')
  const [hasStarted, setHasStarted] = useState(false)
  const [currentPage, setCurrentPage] = useState('landing')
  const [user, setUser] = useState(null)
  const [pendingQuery, setPendingQuery] = useState(null)

  // Apply theme to document
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  // Handle pending query when entering chat
  useEffect(() => {
    if (currentPage === 'chat' && pendingQuery) {
      // Small delay to ensure components are mounted and we don't trigger state updates during render
      const timer = setTimeout(() => {
        handleSendMessage(pendingQuery)
        setPendingQuery(null)
      }, 500)
      return () => clearTimeout(timer)
    }
  }, [currentPage, pendingQuery])

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  // Updated navigation to accept params
  const handleNavigate = (page, params = {}) => {
    setCurrentPage(page)
    if (params.query) {
      setPendingQuery(params.query)
    }
  }

  const handleLogin = (userData) => {
    setUser(userData)
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

  const handleLogout = () => {
    setUser(null)
    setCurrentPage('landing')
    setMessages([])
    setHasStarted(false)
  }

  // Render based on current page
  if (currentPage === 'landing') {
    return <LandingPage onNavigate={handleNavigate} />
  }

  if (currentPage === 'login') {
    return <LoginPage onNavigate={handleNavigate} onLogin={handleLogin} />
  }

  if (currentPage === 'signup') {
    return <SignupPage onNavigate={handleNavigate} onLogin={handleLogin} />
  }

  // Chat page
  return (
    <div className="app">
      <div className="animated-bg"></div>
      <Header
        theme={theme}
        onToggleTheme={toggleTheme}
        onClearChat={clearChat}
        hasMessages={messages.length > 0}
        user={user}
        onLogout={handleLogout}
        onNavigate={handleNavigate}
      />

      <main className="main-container">
        <div className="chat-container glass">
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
