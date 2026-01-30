import './LandingPage.css'

// SVG Icons
const DocumentIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
    </svg>
)

const BoltIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
    </svg>
)

const ShieldIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        <polyline points="9 12 11 14 15 10" />
    </svg>
)

const LayersIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="12 2 2 7 12 12 22 7 12 2" />
        <polyline points="2 17 12 22 22 17" />
        <polyline points="2 12 12 17 22 12" />
    </svg>
)

const ArrowRightIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M5 12h14M12 5l7 7-7 7" />
    </svg>
)

function LandingPage({ onNavigate }) {
    const features = [
        {
            icon: <DocumentIcon />,
            title: 'Official Sources',
            description: 'Get answers from verified SIT documents and policies'
        },
        {
            icon: <BoltIcon />,
            title: 'Instant Answers',
            description: 'AI-powered responses in seconds, not minutes'
        },
        {
            icon: <ShieldIcon />,
            title: 'Zero Hallucinations',
            description: 'Only verified information from official documents'
        },
        {
            icon: <LayersIcon />,
            title: '26+ Documents',
            description: 'Comprehensive coverage of all SIT information'
        }
    ]

    const stats = [
        { value: '26+', label: 'Documents' },
        { value: '1,760', label: 'Knowledge Points' },
        { value: '24/7', label: 'Availability' },
        { value: '100%', label: 'Accuracy' }
    ]

    return (
        <div className="landing-page">
            {/* Animated Background */}
            <div className="animated-bg"></div>

            {/* Navigation */}
            <nav className="landing-nav glass">
                <div className="nav-brand">
                    <div className="nav-logo">
                        <img src="/sit-logo.png" alt="SIT" />
                    </div>
                    <span className="nav-title">SIT Assistant</span>
                </div>
                <div className="nav-actions">
                    <button className="btn btn-ghost" onClick={() => onNavigate('login')}>
                        Sign In
                    </button>
                    <button className="btn btn-primary" onClick={() => onNavigate('signup')}>
                        Get Started
                    </button>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="hero">
                <div className="hero-content">
                    <div className="hero-badge animate-fadeIn">
                        <span className="badge-dot"></span>
                        Powered by AI • Updated January 2026
                    </div>

                    <h1 className="hero-title animate-fadeInUp stagger-1">
                        Your Intelligent Guide to
                        <span className="gradient-text"> SIT Academics</span>
                    </h1>

                    <p className="hero-subtitle animate-fadeInUp stagger-2">
                        Get instant, verified answers about admissions, fees, placements,
                        hostel life, and everything about Siddaganga Institute of Technology.
                    </p>

                    <div className="hero-actions animate-fadeInUp stagger-3">
                        <button className="btn btn-primary btn-lg" onClick={() => onNavigate('chat')}>
                            <span>Start Asking</span>
                            <ArrowRightIcon />
                        </button>
                        <button className="btn btn-secondary btn-lg" onClick={() => onNavigate('login')}>
                            Sign In
                        </button>
                    </div>
                </div>

                {/* Hero Visual */}
                <div className="hero-visual animate-fadeInUp stagger-4">
                    <div className="chat-preview glass">
                        <div className="preview-header">
                            <div className="preview-dots">
                                <span></span><span></span><span></span>
                            </div>
                            <span className="preview-title">SIT Assistant</span>
                        </div>
                        <div className="preview-messages">
                            <div className="preview-message user">
                                What is the fee for CSE branch?
                            </div>
                            <div className="preview-message bot">
                                <p>For CSE (Government Quota), the annual fee is approximately:</p>
                                <p><strong>₹45,000</strong> tuition + <strong>₹15,000</strong> other = <strong>₹60,000/year</strong></p>
                                <span className="source-tag">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                                        <polyline points="14 2 14 8 20 8" />
                                    </svg>
                                    SIT_Fee_Structure.md
                                </span>
                            </div>
                        </div>
                        <div className="preview-glow"></div>
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="stats-section">
                <div className="stats-grid">
                    {stats.map((stat, index) => (
                        <div key={index} className={`stat-item animate-fadeInUp stagger-${index + 1}`}>
                            <span className="stat-value gradient-text">{stat.value}</span>
                            <span className="stat-label">{stat.label}</span>
                        </div>
                    ))}
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
                <div className="section-header">
                    <h2 className="section-title">
                        Everything you need to know about <span className="gradient-text">SIT</span>
                    </h2>
                    <p className="section-subtitle">
                        From admissions to placements, get verified information instantly
                    </p>
                </div>

                <div className="features-grid">
                    {features.map((feature, index) => (
                        <div key={index} className={`feature-card card-glass animate-fadeInUp stagger-${index + 1}`}>
                            <div className="feature-icon">{feature.icon}</div>
                            <h3 className="feature-title">{feature.title}</h3>
                            <p className="feature-desc">{feature.description}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* Topics Section */}
            <section className="topics-section">
                <h2 className="section-title">Ask about anything</h2>
                <div className="topics-grid">
                    {[
                        'Fee Structure', 'Hostel Life', 'Placements', 'Scholarships',
                        'CSE Curriculum', 'Library', 'Labs', 'Clubs & Events',
                        'Admissions', 'Faculty', 'Transport', 'Rules & Regulations'
                    ].map((topic, index) => (
                        <button
                            key={index}
                            className="topic-chip"
                            onClick={() => onNavigate('chat', { query: `Tell me about ${topic}` })}
                        >
                            {topic}
                        </button>
                    ))}
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section">
                <div className="cta-card card-glass">
                    <h2>Ready to get started?</h2>
                    <p>Ask your first question and experience the power of AI-assisted learning</p>
                    <button className="btn btn-primary btn-lg" onClick={() => onNavigate('chat')}>
                        Start Chatting Now
                    </button>
                </div>
            </section>

            {/* Footer */}
            <footer className="landing-footer">
                <p>© 2026 SIT Academic Assistant • Siddaganga Institute of Technology, Tumakuru</p>
            </footer>
        </div>
    )
}

export default LandingPage
