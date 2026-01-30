import './Header.css'

function Header({ theme, onToggleTheme, onClearChat, hasMessages, user, onLogout, onNavigate }) {
    return (
        <header className="header glass">
            <div className="header-brand" onClick={() => onNavigate && onNavigate('landing')}>
                <div className="header-logo">
                    <img src="/sit-logo.png" alt="SIT Logo" />
                </div>
                <div className="header-text">
                    <h1>SIT Assistant</h1>
                    <p>AI-Powered Academic Guide</p>
                </div>
            </div>

            <div className="header-actions">
                {hasMessages && (
                    <button
                        className="header-btn"
                        onClick={onClearChat}
                        title="New conversation"
                        aria-label="New conversation"
                    >
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M12 5v14M5 12h14" />
                        </svg>
                        <span className="btn-label">New Chat</span>
                    </button>
                )}
                <button
                    className="header-btn icon-only"
                    onClick={onToggleTheme}
                    title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
                    aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
                >
                    {theme === 'light' ? (
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
                        </svg>
                    ) : (
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="12" cy="12" r="5" />
                            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
                        </svg>
                    )}
                </button>
                {user ? (
                    <div className="user-menu">
                        <div className="user-avatar">
                            {user.name ? user.name[0].toUpperCase() : 'U'}
                        </div>
                    </div>
                ) : (
                    <button
                        className="header-btn btn-primary-sm"
                        onClick={() => onNavigate && onNavigate('login')}
                    >
                        Sign In
                    </button>
                )}
            </div>
        </header>
    )
}

export default Header
