"""
Pytest configuration and fixtures.
"""
import pytest
import os
import sys
import tempfile
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def temp_kb_file():
    """Create a temporary knowledge base file for testing."""
    test_data = {
        "entries": [
            {
                "name": "Test Person",
                "summary": "A person created for testing purposes."
            },
            {
                "name": "Another Test",
                "summary": "Another entry for comprehensive testing."
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    try:
        os.unlink(temp_file)
    except OSError:
        pass


@pytest.fixture
def sample_queries():
    """Sample queries for testing different tool types."""
    return {
        "calculator": [
            "What is 2 + 2?",
            "12.5% of 243",
            "Add 10 to 5",
            "(10 + 5) * 2"
        ],
        "weather": [
            "Weather in Paris",
            "What is the temperature in London?",
            "How's the weather in Dhaka?"
        ],
        "kb": [
            "Who is Ada Lovelace?",
            "Tell me about Alan Turing",
            "What is machine learning?"
        ],
        "unitconv": [
            "Convert 10 USD to EUR",
            "Convert 100 C to F",
            "Convert 1 M to FT"
        ],
        "translator": [
            'Translate "hello" from English to Spanish',
            'Translate "goodbye" to French',
            'Translate "thank you" from English to German'
        ]
    }


@pytest.fixture(autouse=True)
def ensure_data_directory():
    """Ensure the data directory exists for tests."""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Create default kb.json if it doesn't exist
    kb_file = data_dir / "kb.json"
    if not kb_file.exists():
        default_kb = {
            "entries": [
                {
                    "name": "Ada Lovelace",
                    "summary": "Ada Lovelace was a 19th-century mathematician regarded as an early computing pioneer for her work on Charles Babbage's Analytical Engine."
                },
                {
                    "name": "Alan Turing",
                    "summary": "Alan Turing was a mathematician and logician, widely considered to be the father of theoretical computer science and artificial intelligence."
                }
            ]
        }
        
        with open(kb_file, 'w') as f:
            json.dump(default_kb, f, indent=2)


@pytest.fixture
def mock_agent():
    """Create a mock agent instance for testing."""
    from agent.agent import Agent
    return Agent()


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )