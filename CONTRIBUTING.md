# Contributing to SigmaRecon

Thank you for your interest in contributing to SigmaRecon! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/SigmaRecon.git
   cd SigmaRecon
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

3. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Code Style

- **Python**: Follow PEP 8 style guidelines
- **Line Length**: Maximum 100 characters
- **Type Hints**: Use type hints for all functions
- **Documentation**: Use Google-style docstrings

### Formatting
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Testing

Run the test suite before submitting changes:

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/

# Generate coverage report
pytest --cov=sigmarecon --cov-report=html
```

### Writing Tests

- Write unit tests for new functionality
- Include integration tests for tool integrations
- Add performance tests for critical code paths
- Ensure all tests pass before submitting PR

## Submission Guidelines

### Pull Request Process

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit changes**
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

```
Type: Brief description

Longer description if needed.

Fixes #123
```

**Types:**
- `Add`: New feature
- `Fix`: Bug fix
- `Update`: Modify existing feature
- `Remove`: Delete feature
- `Docs`: Documentation changes
- `Test`: Test-related changes
- `Refactor`: Code refactoring

### Pull Request Requirements

- ✅ All tests pass
- ✅ Code coverage maintained or improved
- ✅ Documentation updated
- ✅ Commit messages follow guidelines
- ✅ No breaking changes (or clearly documented)

## Adding New Tools

To integrate a new subdomain enumeration tool:

1. **Create tool adapter** in `sigmarecon/tools/adapters/`
2. **Inherit from BaseTool**
3. **Implement required methods**
4. **Add tests** in `tests/unit/test_tools/`
5. **Update documentation**

### Example Adapter

```python
from sigmarecon.tools.base import BaseTool

class NewToolAdapter(BaseTool):
    def __init__(self):
        super().__init__(
            name="newtool",
            description="Description of the tool",
            version="1.0.0"
        )
    
    def get_subdomains(self, domain: str, **kwargs) -> List[str]:
        # Implementation here
        pass
```

## Security Guidelines

- **No Secrets**: Never commit API keys, passwords, or tokens
- **Rate Limiting**: Respect target systems in all implementations
- **Ethical Use**: Ensure tools are used for authorized testing only
- **Vulnerability Reporting**: Report security issues privately

## Questions?

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: Contact via GitHub for private matters

Thank you for contributing to SigmaRecon! 🚀