import './WelcomeScreen.css'

const QUICK_QUESTIONS = [
    "What is the fee for CSE branch?",
    "What are the hostel timings and rules?",
    "What is Dasoha and how does free food work?",
    "What scholarships are available?",
    "What is the average placement package?",
    "How do I apply through KCET?"
]

// SVG Icons
const GraduationIcon = () => (
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
        <path d="M6 12v5c3 3 9 3 12 0v-5" />
    </svg>
)

const DocumentIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
    </svg>
)

const CheckIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="20 6 9 17 4 12" />
    </svg>
)

const BoltIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
    </svg>
)

const ChatIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
)

function WelcomeScreen({ onQuickQuestion }) {
    return (
        <div className="welcome-screen">
            <div className="welcome-header animate-fadeIn">
                <div className="welcome-avatar">
                    <span className="avatar-icon">
                        <GraduationIcon />
                    </span>
                    <div className="avatar-pulse"></div>
                </div>

                <h2 className="welcome-title">
                    Welcome to <span className="gradient-text">SIT Assistant</span>
                </h2>

                <p className="welcome-subtitle">
                    Your AI-powered guide to Siddaganga Institute of Technology.
                    Ask me anything about academics, admissions, and campus life.
                </p>
            </div>

            <div className="welcome-features animate-fadeInUp stagger-1">
                <div className="feature-pill">
                    <span className="pill-icon"><DocumentIcon /></span>
                    <span>26+ Documents</span>
                </div>
                <div className="feature-pill">
                    <span className="pill-icon"><CheckIcon /></span>
                    <span>Verified Info</span>
                </div>
                <div className="feature-pill">
                    <span className="pill-icon"><BoltIcon /></span>
                    <span>Instant</span>
                </div>
            </div>

            <div className="quick-questions animate-fadeInUp stagger-2">
                <h3>Try asking</h3>
                <div className="quick-question-grid">
                    {QUICK_QUESTIONS.map((question, index) => (
                        <button
                            key={index}
                            className="quick-question-btn"
                            onClick={() => onQuickQuestion(question)}
                        >
                            <span className="question-icon"><ChatIcon /></span>
                            <span>{question}</span>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default WelcomeScreen
