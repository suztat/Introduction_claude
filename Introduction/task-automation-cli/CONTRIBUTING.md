# Contributing to Task Automation CLI

Thank you for your interest in contributing to Task Automation CLI! 🎉

We welcome contributions of all kinds: bug reports, feature requests, documentation improvements, and code contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)

## Code of Conduct

This project adheres to a simple code of conduct:

- **Be respectful** and considerate in your communication
- **Be collaborative** and help others learn
- **Be open** to constructive feedback
- **Focus on what is best** for the community and the project

## How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
1. **Check existing issues** to avoid duplicates
2. **Try the latest version** to see if the bug has been fixed
3. **Collect information** about the bug

When submitting a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs. actual behavior
- **Python version** and operating system
- **Error messages** or stack traces (if applicable)
- **Sample code or data** if relevant

**Example bug report:**

```markdown
### Bug: Task IDs duplicate after deletion

**Environment:**
- Python 3.9.5
- macOS 12.3
- Task Automation CLI v1.0.0

**Steps to reproduce:**
1. Add 3 tasks
2. Delete task #2
3. Add a new task
4. New task gets ID #3 (duplicate)

**Expected:** New task should get ID #4
**Actual:** New task gets ID #3

**Error message:** None, but causes data conflicts
```

### Suggesting Features

We love feature suggestions! To suggest a new feature:

1. **Check existing issues** for similar requests
2. **Describe the problem** your feature would solve
3. **Explain your proposed solution**
4. **Consider alternatives** you've thought about

**Example feature request:**

```markdown
### Feature: Add task sorting by priority

**Problem:**
Currently, tasks are displayed in the order they were created. For users with many tasks, it's hard to see urgent items at a glance.

**Proposed solution:**
Add a `--sort` flag to the `list` command:
- `--sort priority` - Show urgent → high → medium → low
- `--sort date` - Default (current behavior)

**Alternatives considered:**
- Always sort by priority (but this removes flexibility)
- Add a config file for default sorting (more complex)

**Benefits:**
- Easier to focus on important tasks
- More flexible task management
```

### Submitting Pull Requests

We welcome pull requests! Here's how to submit one:

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Introduction_claude.git
cd Introduction_claude/Introduction/task-automation-cli
```

#### 2. Create a Branch

```bash
# Create a descriptive branch name
git checkout -b feature/add-task-sorting
# or
git checkout -b fix/duplicate-task-ids
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `test/` - Test improvements
- `refactor/` - Code refactoring

#### 3. Make Your Changes

- Follow our [coding standards](#coding-standards)
- Add tests for new features
- Update documentation as needed
- Keep changes focused and atomic

#### 4. Test Your Changes

```bash
# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest --cov=task_cli tests/

# Check code style
black --check task_cli.py tests/
flake8 task_cli.py tests/
```

#### 5. Commit Your Changes

Follow our [commit message guidelines](#commit-message-guidelines):

```bash
git add .
git commit -m "feat: Add task sorting by priority"
```

#### 6. Push and Create PR

```bash
# Push your branch
git push origin feature/add-task-sorting

# Create a Pull Request on GitHub with:
# - Clear title
# - Description of changes
# - Reference to related issues
```

**Pull Request Template:**

```markdown
## Description
Brief description of what this PR does

## Related Issue
Fixes #123

## Changes Made
- Added X feature
- Fixed Y bug
- Updated Z documentation

## Testing
- [ ] Added unit tests
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Commit messages follow guidelines
```

## Development Setup

### 1. Install Python

Ensure you have Python 3.6+ installed:

```bash
python --version  # or python3 --version
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install development dependencies
pip install -r requirements.txt

# Install development tools (optional)
pip install black flake8 pytest pytest-cov
```

### 4. Verify Setup

```bash
# Run tests to verify everything works
python -m pytest tests/ -v
```

## Coding Standards

### Python Style Guide

- Follow **PEP 8** style guide
- Use **Black** for code formatting (line length: 88)
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions and classes

### Code Formatting

```bash
# Format code with Black
black task_cli.py tests/

# Check formatting
black --check task_cli.py tests/
```

### Linting

```bash
# Run flake8
flake8 task_cli.py tests/
```

### Example Code Style

```python
from typing import List, Dict, Optional


def add_task(description: str, priority: str = "medium") -> Dict:
    """
    Add a new task with the given description and priority.

    Args:
        description: The task description
        priority: Task priority level (low, medium, high, urgent)

    Returns:
        A dictionary containing the created task data

    Raises:
        ValueError: If priority is not valid

    Example:
        >>> task = add_task("Fix bug", priority="high")
        >>> print(task["description"])
        Fix bug
    """
    # Implementation here
    pass
```

## Commit Message Guidelines

We follow the **Conventional Commits** specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Feature
git commit -m "feat: Add task sorting by priority"

# Bug fix
git commit -m "fix: Prevent duplicate task IDs after deletion"

# Documentation
git commit -m "docs: Add troubleshooting section to README"

# With body
git commit -m "feat: Add urgent priority level

- Add urgent priority option to CLI
- Update README with urgent priority docs
- Add tests for urgent priority"
```

### Breaking Changes

If your change breaks backward compatibility, add `BREAKING CHANGE:` in the footer:

```bash
git commit -m "feat: Change task storage format

BREAKING CHANGE: Tasks now stored in v2 format.
Run migration script to convert existing tasks."
```

## Testing Guidelines

### Writing Tests

- **One test per behavior** - Each test should verify one specific behavior
- **Descriptive names** - Test names should clearly describe what they test
- **AAA pattern** - Arrange, Act, Assert
- **Use fixtures** - Leverage pytest fixtures for setup

### Test Structure

```python
def test_add_task_with_urgent_priority(self, task_manager):
    """Test adding a task with urgent priority."""
    # Arrange
    description = "Fix critical bug"
    priority = "urgent"

    # Act
    task = task_manager.add_task(description, priority)

    # Assert
    assert task["description"] == description
    assert task["priority"] == "urgent"
    assert task["completed"] is False
```

### Test Coverage

- Aim for **80%+ code coverage**
- Focus on **critical paths** and **edge cases**
- Test **both success and failure** scenarios

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_task_cli.py -v

# Run specific test
python -m pytest tests/test_task_cli.py::TestTaskManager::test_add_task -v

# Check coverage
python -m pytest --cov=task_cli --cov-report=term-missing tests/
```

## Documentation Guidelines

### Code Documentation

- **Docstrings** for all public functions and classes
- **Inline comments** for complex logic only
- **Type hints** for better code clarity

### Documentation Files

When updating documentation:

- **README.md** - User-facing documentation
- **CONTRIBUTING.md** - Contribution guidelines (this file)
- **API docs** - In code via docstrings

### Documentation Style

- Use **clear, concise language**
- Provide **examples** for complex features
- Keep **code snippets** up to date
- Use **Markdown** formatting consistently

## Questions?

If you have questions about contributing:

1. Check existing **Issues** and **Pull Requests**
2. Open a new **Issue** with your question
3. Tag it with the `question` label

---

Thank you for contributing to Task Automation CLI! 🚀

Your contributions make this project better for everyone.
