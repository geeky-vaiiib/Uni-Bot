import './QuickSuggestions.css'

const QUICK_SUGGESTIONS = [
    "Attendance requirement?",
    "What is Dasoha?",
    "Placement packages?",
    "Hostel fees?",
    "Admission process?",
    "Grading system?"
]

function QuickSuggestions({ onSelect }) {
    return (
        <div className="quick-suggestions">
            <span className="suggestions-label">Quick:</span>
            <div className="suggestions-scroll">
                {QUICK_SUGGESTIONS.map((q, i) => (
                    <button
                        key={i}
                        className="suggestion-chip"
                        onClick={() => onSelect(q)}
                    >
                        {q}
                    </button>
                ))}
            </div>
        </div>
    )
}

export default QuickSuggestions
