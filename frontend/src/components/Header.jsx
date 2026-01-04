import './Header.css'

function Header({ theme, onToggleTheme, onClearChat, hasMessages }) {
    return (
        <header className="header">
            <div className="header-brand">
                <div className="header-logo">
                    <img src="/sit-logo.png" alt="SIT Logo" />
                </div>
                <div className="header-text">
                    <h1>SIT Academic Assistant</h1>
                    <p>Siddaganga Institute of Technology, Tumakuru</p>
                </div>
            </div>

            <div className="header-actions">
                {hasMessages && (
                    <button
                        className="header-btn clear-btn"
                        onClick={onClearChat}
                        title="Clear conversation"
                        aria-label="Clear conversation"
                    >
                        ✕
                    </button>
                )}
                <button
                    className="header-btn"
                    onClick={onToggleTheme}
                    title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
                    aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
                >
                    {theme === 'light' ? '🌙' : '☀️'}
                </button>
            </div>
        </header>
    )
}

export default Header
