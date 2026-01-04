"""
SIT RAG Chatbot - API Tests
Test suite for the chatbot API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the app
import sys
sys.path.insert(0, str(__file__).replace("/tests/test_api.py", ""))

from app.main import app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


class TestHealthEndpoints:
    """Tests for health check endpoints."""
    
    def test_root_returns_healthy(self, client):
        """Test root endpoint returns healthy status."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "SIT RAG Chatbot"
    
    def test_health_endpoint(self, client):
        """Test dedicated health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestAskEndpoint:
    """Tests for the /api/ask endpoint."""
    
    def test_ask_requires_question(self, client):
        """Test that question is required."""
        response = client.post("/api/ask", json={})
        assert response.status_code == 422  # Validation error
    
    def test_ask_validates_question_length(self, client):
        """Test minimum question length validation."""
        response = client.post("/api/ask", json={"question": "ab"})
        assert response.status_code == 422
    
    def test_ask_accepts_valid_modes(self, client):
        """Test that valid modes are accepted."""
        valid_modes = ["student", "exam", "faculty"]
        for mode in valid_modes:
            response = client.post(
                "/api/ask",
                json={"question": "What is SIT?", "mode": mode}
            )
            # May fail due to missing API key, but should not be 422
            assert response.status_code != 422 or "mode" not in str(response.json())
    
    def test_ask_rejects_invalid_mode(self, client):
        """Test that invalid modes are rejected."""
        response = client.post(
            "/api/ask",
            json={"question": "What is SIT?", "mode": "invalid_mode"}
        )
        assert response.status_code == 422


class TestQueryModes:
    """Tests for query mode functionality."""
    
    def test_default_mode_is_student(self):
        """Test that default query mode is student."""
        from app.models import AskRequest
        request = AskRequest(question="Test question")
        assert request.mode.value == "student"


# Example test queries for manual testing
EXAMPLE_TEST_QUERIES = [
    # Student queries
    {
        "question": "What is the minimum attendance requirement at SIT?",
        "mode": "student",
        "expected_behavior": "Should return attendance policy from academic regulations"
    },
    {
        "question": "How do I apply for a leave of absence?",
        "mode": "student",
        "expected_behavior": "Should provide leave application procedure or refusal"
    },
    
    # Exam queries
    {
        "question": "What is the grading system at SIT?",
        "mode": "exam",
        "expected_behavior": "Should return exact grading scheme from regulations"
    },
    {
        "question": "How can I apply for revaluation?",
        "mode": "exam",
        "expected_behavior": "Should provide revaluation procedure or refusal"
    },
    
    # Faculty queries
    {
        "question": "What is the role of the Board of Studies?",
        "mode": "faculty",
        "expected_behavior": "Should describe BoS composition and functions"
    },
    
    # Out of scope queries (should refuse)
    {
        "question": "What is the weather like today?",
        "mode": "student",
        "expected_behavior": "Should refuse as out of scope"
    },
    {
        "question": "Can you help me with my homework?",
        "mode": "student",
        "expected_behavior": "Should refuse as out of scope"
    },
    
    # Hallucination test queries (should refuse if not in documents)
    {
        "question": "What is the exact fee for B.E. Computer Science in 2025?",
        "mode": "student",
        "expected_behavior": "Should only answer if fee info is in documents, else refuse"
    },
    {
        "question": "Who is the current principal of SIT?",
        "mode": "student",
        "expected_behavior": "Should only answer if in documents, else refuse"
    }
]


def print_test_queries():
    """Print example test queries for manual testing."""
    print("\n" + "="*60)
    print("EXAMPLE TEST QUERIES FOR SIT RAG CHATBOT")
    print("="*60)
    
    for i, query in enumerate(EXAMPLE_TEST_QUERIES, 1):
        print(f"\n{i}. Question: {query['question']}")
        print(f"   Mode: {query['mode']}")
        print(f"   Expected: {query['expected_behavior']}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    print_test_queries()
    pytest.main([__file__, "-v"])
