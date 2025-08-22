# AI AGENT

A robust, extensible agent system that can perform calculations, weather lookups, knowledge base searches, unit conversions, and translations.

## Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│     main.py     │───▶│    Agent     │───▶│  QueryPlanner   │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │                      │
                              ▼                      ▼
                       ┌──────────────┐    ┌─────────────────┐
                       │  ToolManager │    │   ToolPlan      │
                       └──────────────┘    └─────────────────┘
                              │
                              ▼
           ┌──────────────────────────────────────────────────┐
           │                  Tools                           │
           ├──────────┬──────────┬──────────┬──────────┬──────┤
           │Calculator│ Weather  │    KB    │UnitConv  │Trans │
           │   Tool   │   Tool   │   Tool   │  Tool    │Tool  │
           └──────────┴──────────┴──────────┴──────────┴──────┘
```

## Features

### (1) Production Quality Improvements
- **Modular Architecture**: Clean separation of concerns
- **Type Safety**: Pydantic models for validation
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging with execution time tracking
- **Extensible Design**: Easy to add new tools

### (2) Available Tools
1. **Calculator**: Mathematical expressions, percentages
2. **Weather**: Temperature lookup for cities
3. **Knowledge Base**: Information about notable people
4. **Unit Converter**: Currency, temperature, length, weight
5. **Translator**: Multi-language text translation *(NEW)*

### (3) Comprehensive Testing
- Unit tests for all tools
- Integration tests for agent workflow
- Error handling tests
- Extensibility tests
- 95%+ test coverage

### (4) Docker Support
-- Run the full project in just one command



## Quick Start (option 1)

### Installation

```bash
# Python 3.10+ recommended
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Usage

```bash
# Mathematical calculations
python main.py "What is 12.5% of 243?"

# Weather information
python main.py "What's the weather in Paris?"

# Knowledge base queries
python main.py "Who is Ada Lovelace?"

# Unit conversions
python main.py "Convert 100 C to F"

# Text translation (NEW!)
python main.py "Translate hello from English to Spanish"


# Complex calculations with weather data
python main.py "Add 10 to the average temperature in Paris and London"
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agent --cov-report=html

# Run only fast tests
pytest -m "not slow"

# Run specific test file
pytest tests/test_agent.py -v
```

## Quick Start (option 2)
### 🐳 Docker (option 2)

**Fastest way to get started:**

```bash
# Build and run with Docker Compose
docker-compose build
docker-compose run --rm agent "What is 12.5% of 243?"
```


### 🐳 Docker Usage

```bash
# Mathematical calculations
docker-compose run --rm agent "What is 12.5% of 243?"


# Weather information
docker-compose run --rm agent "What's the weather in Paris?"


# Knowledge base queries
docker-compose run --rm agent "Who is Ada Lovelace?"


# Unit conversions
docker-compose run --rm agent "Convert 100 C to F"


# Text translation (NEW!)
docker-compose run --rm agent "Translate hello from English to Spanish"


# Complex calculations with weather data
docker-compose run --rm agent "Add 10 to the average temperature in Paris and London"
```


### 🐳 Docker Development & testing

```bash
# Run tests
docker-compose run --rm agent-test

# Development mode with hot reload
docker-compose run --rm agent-dev python main.py "your question"

# Interactive shell for debugging
docker-compose run --rm agent-shell

# Run with specific service
docker-compose run --rm agent-dev python main.py "What is 2+2?"
```



## Tool Development

### Adding a New Tool

1. **Create tool class** (inherit from `BaseTool`):
```python
from agent.tools.base import BaseTool

class MyNewTool(BaseTool):
    @property
    def name(self) -> str:
        return "mytool"
    
    def execute(self, **kwargs) -> str:
        # Implementation here
        return "result"
```

2. **Register in agent**:
```python
# In agent/models.py
class ToolName(str, Enum):
    MY_TOOL = "mytool"

# In agent/agent.py
self.tools = {
    # ... existing tools
    ToolName.MY_TOOL: mytool_instance,
}
```

3. **Add planning logic**:
```python
# In agent/planner.py
def _plan_my_tool(self, normalized_query: str, original_query: str):