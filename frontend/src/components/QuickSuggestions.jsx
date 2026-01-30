import './QuickSuggestions.css'

const QUICK_SUGGESTIONS = [
    "Attendance requirement?",
    "Placement packages?",
    "Hostel fees?",
    "Admission process?",
    "Grading system?",
    "Library timings?",
    "Bus routes?",
    "Dress code?",
    "Exam schedule?"
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
