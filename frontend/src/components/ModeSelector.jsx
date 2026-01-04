import './ModeSelector.css'

const MODES = [
    { id: 'student', label: 'Student', icon: '🎓' },
    { id: 'exam', label: 'Exam', icon: '📝' },
    { id: 'faculty', label: 'Faculty', icon: '👔' }
]

function ModeSelector({ mode, onModeChange }) {
    return (
        <div className="mode-selector">
            <span className="mode-label">Query Mode:</span>
            <div className="mode-options" role="group" aria-label="Select query mode">
                {MODES.map((m) => (
                    <button
                        key={m.id}
                        className={`mode-btn ${mode === m.id ? 'active' : ''}`}
                        onClick={() => onModeChange(m.id)}
                        aria-pressed={mode === m.id}
                        title={`${m.label} mode - Optimized for ${m.label.toLowerCase()} queries`}
                    >
                        <span className="mode-icon">{m.icon}</span>
                        <span className="mode-text">{m.label}</span>
                    </button>
                ))}
            </div>
        </div>
    )
}

export default ModeSelector
