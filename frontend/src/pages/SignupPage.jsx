import { useState } from 'react'
import './AuthPages.css'

function SignupPage({ onNavigate, onLogin }) {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
    })
    const [isLoading, setIsLoading] = useState(false)
    const [agreedToTerms, setAgreedToTerms] = useState(false)

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({ ...prev, [name]: value }))
    }

    const getPasswordStrength = () => {
        const { password } = formData
        if (!password) return { level: 0, text: '', color: '' }
        if (password.length < 6) return { level: 1, text: 'Weak', color: '#ef4444' }
        if (password.length < 8) return { level: 2, text: 'Fair', color: '#f59e0b' }
        if (password.length >= 8 && /[A-Z]/.test(password) && /[0-9]/.test(password)) {
            return { level: 4, text: 'Strong', color: '#10b981' }
        }
        return { level: 3, text: 'Good', color: '#e6be8a' }
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        if (formData.password !== formData.confirmPassword) {
            alert('Passwords do not match')
            return
        }
        setIsLoading(true)
        // Simulate signup - in production, this would call an API
        setTimeout(() => {
            setIsLoading(false)
            // Pass user data to parent
            onLogin({ name: formData.name, email: formData.email })
            onNavigate('chat')
        }, 1500)
    }

    const strength = getPasswordStrength()

    return (
        <div className="auth-page">
            <div className="animated-bg"></div>

            <div className="auth-container">
                {/* Left Side - Branding */}
                <div className="auth-branding">
                    <div className="branding-content">
                        <div className="branding-logo" onClick={() => onNavigate('landing')}>
                            <img src="/sit-logo.png" alt="SIT" />
                        </div>
                        <h1 className="branding-title">
                            Join the
                            <span className="gradient-text"> SIT Community</span>
                        </h1>
                        <p className="branding-subtitle">
                            Get instant answers to all your questions about Siddaganga Institute of Technology
                        </p>

                        <div className="branding-features">
                            <div className="branding-feature">
                                <span className="feature-check">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                                        <polyline points="20 6 9 17 4 12" />
                                    </svg>
                                </span>
                                <span>Personalized Experience</span>
                            </div>
                            <div className="branding-feature">
                                <span className="feature-check">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                                        <polyline points="20 6 9 17 4 12" />
                                    </svg>
                                </span>
                                <span>Save Conversations</span>
                            </div>
                            <div className="branding-feature">
                                <span className="feature-check">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                                        <polyline points="20 6 9 17 4 12" />
                                    </svg>
                                </span>
                                <span>Priority Support</span>
                            </div>
                        </div>
                    </div>

                    <div className="branding-glow"></div>
                </div>

                {/* Right Side - Form */}
                <div className="auth-form-container">
                    <div className="auth-form-wrapper card-glass">
                        <div className="auth-header">
                            <h2>Create Account</h2>
                            <p>Start your journey with SIT Assistant</p>
                        </div>

                        <form className="auth-form" onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label htmlFor="name">Full Name</label>
                                <input
                                    type="text"
                                    id="name"
                                    name="name"
                                    className="input"
                                    placeholder="Your full name"
                                    value={formData.name}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="email">Email</label>
                                <input
                                    type="email"
                                    id="email"
                                    name="email"
                                    className="input"
                                    placeholder="your.email@sit.ac.in"
                                    value={formData.email}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="password">Password</label>
                                <input
                                    type="password"
                                    id="password"
                                    name="password"
                                    className="input"
                                    placeholder="Create a strong password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    required
                                />
                                {formData.password && (
                                    <div className="password-strength">
                                        <div className="strength-bar">
                                            {[1, 2, 3, 4].map(level => (
                                                <div
                                                    key={level}
                                                    className={`strength-segment ${level <= strength.level ? 'active' : ''}`}
                                                    style={{ backgroundColor: level <= strength.level ? strength.color : '' }}
                                                />
                                            ))}
                                        </div>
                                        <span className="strength-text" style={{ color: strength.color }}>
                                            {strength.text}
                                        </span>
                                    </div>
                                )}
                            </div>

                            <div className="form-group">
                                <label htmlFor="confirmPassword">Confirm Password</label>
                                <input
                                    type="password"
                                    id="confirmPassword"
                                    name="confirmPassword"
                                    className="input"
                                    placeholder="Confirm your password"
                                    value={formData.confirmPassword}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <label className="checkbox-label terms-checkbox">
                                <input
                                    type="checkbox"
                                    checked={agreedToTerms}
                                    onChange={(e) => setAgreedToTerms(e.target.checked)}
                                    required
                                />
                                <span>
                                    I agree to the <button type="button" className="text-link">Terms of Service</button> and{' '}
                                    <button type="button" className="text-link">Privacy Policy</button>
                                </span>
                            </label>

                            <button
                                type="submit"
                                className={`btn btn-primary btn-full ${isLoading ? 'loading' : ''}`}
                                disabled={isLoading || !agreedToTerms}
                            >
                                {isLoading ? (
                                    <span className="spinner"></span>
                                ) : (
                                    'Create Account'
                                )}
                            </button>
                        </form>

                        <div className="auth-divider">
                            <span>or sign up with</span>
                        </div>

                        <div className="social-buttons">
                            <button className="btn btn-secondary social-btn">
                                <svg width="20" height="20" viewBox="0 0 24 24">
                                    <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                                    <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                                    <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                                    <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                                </svg>
                                Google
                            </button>
                            <button className="btn btn-secondary social-btn">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                                </svg>
                                GitHub
                            </button>
                        </div>

                        <p className="auth-footer">
                            Already have an account?{' '}
                            <button className="text-link" onClick={() => onNavigate('login')}>
                                Sign in
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SignupPage
