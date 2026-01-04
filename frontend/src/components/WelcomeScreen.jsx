import './WelcomeScreen.css'

const QUICK_QUESTIONS = [
    "What is the minimum attendance requirement at SIT?",
    "What is Dasoha and how does free food work?",
    "What is the average placement package and which companies visit?",
    "What are the hostel facilities and fees?",
    "How do I apply for admission through KCET?",
    "What are the eligibility criteria for B.E. programs?"
]

function WelcomeScreen({ onQuickQuestion }) {
    return (
        <div className="welcome-screen">
            <div className="welcome-icon">
                🎓
            </div>

            <h2 className="welcome-title">
                Welcome to <span className="highlight">SIT Assistant</span>
            </h2>

            <p className="welcome-subtitle">
                Your intelligent guide to academics, admissions, and policies at
                Siddaganga Institute of Technology. Get instant, verified answers
                from official documents.
            </p>

            <div className="welcome-features">
                <div className="feature-badge">
                    <span className="feature-icon">📚</span>
                    Official Documents
                </div>
                <div className="feature-badge">
                    <span className="feature-icon">✓</span>
                    Verified Info
                </div>
                <div className="feature-badge">
                    <span className="feature-icon">⚡</span>
                    Instant Answers
                </div>
                <div className="feature-badge">
                    <span className="feature-icon">🔒</span>
                    Zero Hallucinations
                </div>
            </div>

            <div className="quick-questions">
                <h3>Try asking</h3>
                <div className="quick-question-grid">
                    {QUICK_QUESTIONS.map((question, index) => (
                        <button
                            key={index}
                            className="quick-question-btn"
                            onClick={() => onQuickQuestion(question)}
                        >
                            {question}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default WelcomeScreen
