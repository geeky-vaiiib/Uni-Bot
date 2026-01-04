"""
SIT RAG Chatbot - Query Modes
Different instruction sets for Student, Exam-oriented, and Faculty/Admin queries.
"""

from enum import Enum
from typing import Literal


QueryModeType = Literal["student", "exam", "faculty"]


class QueryMode(Enum):
    """Query mode enumeration with associated instructions."""
    
    STUDENT = "student"
    EXAM = "exam"
    FACULTY = "faculty"


# Mode-specific instructions to append to the context prompt
MODE_INSTRUCTIONS = {
    "student": """
MODE: STUDENT QUERY
- Provide clear, student-friendly explanations.
- Focus on practical steps and actionable information.
- Explain procedures in step-by-step format when applicable.
- Use simple language while maintaining formal tone.
- Highlight important deadlines or requirements.
- If referring to forms or applications, mention where to obtain them.
""",
    
    "exam": """
MODE: EXAMINATION QUERY
- Prioritize accuracy for exam-related information.
- Focus on: exam schedules, eligibility, marks, grading, revaluation, and results.
- Reference the Controller of Examinations (CoE) when applicable.
- For eligibility queries, cite specific attendance or internal marks requirements.
- For grading queries, cite the exact grading scheme from SIT regulations.
- NEVER estimate or calculate marks/grades without exact data from documents.
- Always recommend verification with the Examination Section for critical queries.
""",
    
    "faculty": """
MODE: FACULTY/ADMINISTRATION QUERY
- Provide detailed, policy-oriented responses.
- Reference relevant committees (GC, AC, BoS, IQAC, IAAC) when applicable.
- Include regulatory and compliance aspects when relevant.
- Use formal institutional language.
- For policy queries, cite the specific regulation section.
- For curriculum or syllabus queries, reference Board of Studies (BoS) decisions.
- Mention approval bodies (AC, GC) for academic changes.
"""
}


def get_mode_instruction(mode: QueryModeType) -> str:
    """
    Get the mode-specific instruction for the given query mode.
    
    Args:
        mode: Query mode (student, exam, or faculty)
    
    Returns:
        Mode-specific instruction string
    """
    return MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS["student"])


def get_all_modes() -> list:
    """Get list of all available query modes."""
    return list(MODE_INSTRUCTIONS.keys())
