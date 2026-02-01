# Task Automation CLI

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple, lightweight command-line task management tool written in Python. Manage your daily tasks efficiently from the terminal with priority levels, completion tracking, and persistent storage.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Add a Task](#add-a-task)
  - [List Tasks](#list-tasks)
  - [Complete a Task](#complete-a-task)
  - [Delete a Task](#delete-a-task)
- [Priority Levels](#priority-levels)
- [Examples](#examples)
- [Data Storage](#data-storage)
- [Testing](#testing)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

## Features

- ✅ **Add tasks** with priorities (low, medium, high, urgent)
- 📋 **List** active and completed tasks
- ✓ **Mark tasks** as completed with timestamps
- 🗑️ **Delete** tasks you no longer need
- 💾 **Persistent storage** in JSON format
- 🎨 **Color-coded priority indicators** for quick visual scanning
- 🚀 **Fast and lightweight** - no database required
- 🔧 **Easy to integrate** into shell scripts and workflows

## Quick Start

```bash
# Clone the repository
git clone https://github.com/suztat/Introduction_claude.git
cd Introduction_claude/Introduction/task-automation-cli

# Install dependencies (optional, only needed for development/testing)
pip install -r requirements.txt

# Add your first task
python task_cli.py add "Complete the project documentation" -p high

# List all tasks
python task_cli.py list

# Complete a task
python task_cli.py complete 1

# You're ready to go! 🎉
```

## Installation

### Prerequisites

- **Python 3.6 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (usually comes with Python)

### Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/suztat/Introduction_claude.git
   cd Introduction_claude/Introduction/task-automation-cli
   ```

2. **(Optional) Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **(Optional) Install dependencies:**

   The CLI tool has no runtime dependencies! Dependencies are only needed for development and testing.

   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Make the script executable:**
   ```bash
   chmod +x task_cli.py
   ```

5. **(Optional) Create an alias for easier access:**

   Add to your `~/.bashrc`, `~/.zshrc`, or equivalent:
   ```bash
   alias task='python /path/to/task_cli.py'
   ```

   Then reload your shell configuration:
   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

   Now you can use:
   ```bash
   task add "My new task"
   task list
   ```

## Usage

### Add a Task

Add tasks with optional priority levels:

```bash
# Add a task with default priority (medium)
python task_cli.py add "Finish project documentation"

# Add an urgent task
python task_cli.py add "Fix critical production bug" -p urgent

# Add a high priority task
python task_cli.py add "Review pull requests" -p high

# Add a low priority task
python task_cli.py add "Update dependencies" --priority low
```

**Options:**
- `-p, --priority {low,medium,high,urgent}` - Set task priority (default: medium)

### List Tasks

View your tasks in different ways:

```bash
# List active tasks only (default)
python task_cli.py list

# List all tasks (including completed)
python task_cli.py list --all
python task_cli.py list -a
```

**Options:**
- `-a, --all` - Show completed tasks as well

### Complete a Task

Mark a task as completed:

```bash
python task_cli.py complete 1
```

**Arguments:**
- `task_id` - The ID number of the task to complete (shown in list output)

### Delete a Task

Permanently remove a task:

```bash
python task_cli.py delete 2
```

**Arguments:**
- `task_id` - The ID number of the task to delete (shown in list output)

## Priority Levels

Tasks support four priority levels, each with a distinct visual indicator:

| Priority | Symbol | Description | Use Case |
|----------|--------|-------------|----------|
| **Urgent** | 🚨 | Critical and time-sensitive | Production bugs, urgent deadlines |
| **High** | 🔴 | Important tasks | Important features, reviews |
| **Medium** | 🟡 | Normal priority (default) | Regular tasks, improvements |
| **Low** | 🟢 | Nice-to-have | Documentation, refactoring |

## Examples

### Complete Workflow Example

```bash
# Add several tasks with different priorities
$ python task_cli.py add "Fix login bug" -p urgent
✓ Task added: [1] ○ 🚨 Fix login bug

$ python task_cli.py add "Write unit tests" -p high
✓ Task added: [2] ○ 🔴 Write unit tests

$ python task_cli.py add "Update README" -p medium
✓ Task added: [3] ○ 🟡 Update README

$ python task_cli.py add "Refactor old code" -p low
✓ Task added: [4] ○ 🟢 Refactor old code

# List all active tasks
$ python task_cli.py list

Active Tasks:
--------------------------------------------------
[1] ○ 🚨 Fix login bug
[2] ○ 🔴 Write unit tests
[3] ○ 🟡 Update README
[4] ○ 🟢 Refactor old code
--------------------------------------------------
Total: 4 task(s)

# Complete the urgent task
$ python task_cli.py complete 1
✓ Task completed: [1] ✓ 🚨 Fix login bug

# View all tasks including completed
$ python task_cli.py list -a

All Tasks:
--------------------------------------------------
[1] ✓ 🚨 Fix login bug
[2] ○ 🔴 Write unit tests
[3] ○ 🟡 Update README
[4] ○ 🟢 Refactor old code
--------------------------------------------------
Total: 4 task(s)

# Delete a task you no longer need
$ python task_cli.py delete 4
✓ Task 4 deleted.
```

### Integration with Shell Scripts

```bash
#!/bin/bash
# daily-standup.sh - Show today's tasks

echo "📋 Today's Tasks:"
python task_cli.py list

echo ""
echo "✓ Completed Tasks:"
python task_cli.py list -a | grep "✓"
```

## Data Storage

Tasks are stored in a `tasks.json` file in the current working directory. The file is automatically created when you add your first task.

**File location:** `./tasks.json`

**Data structure:**
```json
[
  {
    "id": 1,
    "description": "Fix login bug",
    "priority": "urgent",
    "completed": false,
    "created_at": "2026-02-01T23:00:00.123456",
    "completed_at": null
  }
]
```

### Backup Your Tasks

Since tasks are stored in a simple JSON file, backing up is easy:

```bash
# Backup tasks
cp tasks.json tasks.backup.json

# Restore from backup
cp tasks.backup.json tasks.json
```

## Testing

This project includes comprehensive unit tests using pytest.

### Run Tests

```bash
# Run all tests
python -m pytest tests/

# Run tests with verbose output
python -m pytest tests/ -v

# Run tests with coverage report
python -m pytest --cov=task_cli tests/

# Run tests with coverage HTML report
python -m pytest --cov=task_cli --cov-report=html tests/
```

### Test Coverage

The test suite covers:
- ✓ Task creation and management
- ✓ Data persistence
- ✓ All priority levels
- ✓ Task completion and deletion
- ✓ Edge cases and error handling
- ✓ File I/O operations

## Development

### Project Structure

```
task-automation-cli/
├── task_cli.py          # Main CLI application
├── tests/               # Test files
│   └── test_task_cli.py # Unit tests
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── CONTRIBUTING.md      # Contribution guidelines
├── LICENSE              # MIT License
└── .gitignore          # Git ignore rules
```

### Code Style

This project follows Python best practices:
- **PEP 8** style guide
- **Black** code formatter
- **Type hints** for better code clarity
- **Docstrings** for all public functions

### Running Code Quality Tools

```bash
# Format code with Black
black task_cli.py tests/

# Lint with flake8
flake8 task_cli.py tests/
```

## Troubleshooting

### Common Issues

#### Tasks file not found
**Problem:** `FileNotFoundError` when running commands

**Solution:** The tasks.json file is created automatically. Make sure you have write permissions in the current directory.

```bash
# Check directory permissions
ls -la
```

#### Python version issues
**Problem:** Script doesn't run or shows syntax errors

**Solution:** Ensure you're using Python 3.6 or higher:

```bash
python --version
# or
python3 --version
```

#### Invalid priority value
**Problem:** Error when adding a task with custom priority

**Solution:** Use only valid priorities: `low`, `medium`, `high`, or `urgent`

```bash
# Correct
python task_cli.py add "My task" -p high

# Incorrect
python task_cli.py add "My task" -p critical  # ❌ Not a valid priority
```

#### Task ID not found
**Problem:** "Task ID X not found" when completing/deleting

**Solution:** Run `list` to see all task IDs, then use the correct ID:

```bash
python task_cli.py list
python task_cli.py complete <correct-id>
```

## FAQ

**Q: Can I use this tool on Windows?**
A: Yes! Python runs on Windows. Just make sure Python is installed and in your PATH.

**Q: Where are my tasks stored?**
A: In a `tasks.json` file in the current working directory. You can back it up or move it as needed.

**Q: Can I run this from anywhere on my system?**
A: Yes! Create a shell alias or add the script to your PATH. See the [Installation](#installation) section for details.

**Q: Does this require an internet connection?**
A: No, it's completely offline. All data is stored locally.

**Q: Can I export my tasks?**
A: Tasks are stored in standard JSON format, so you can easily parse, export, or integrate with other tools.

**Q: How do I sync tasks across multiple machines?**
A: You can place the `tasks.json` file in a cloud-synced folder (Dropbox, Google Drive, etc.) or use version control (Git).

**Q: Can I customize the priority levels or emojis?**
A: Yes! The code is open source. Edit the `priority_symbols` dictionary in `task_cli.py` to customize.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to:

- Report bugs
- Suggest features
- Submit pull requests
- Follow our code of conduct

Quick contribution steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python -m pytest tests/`)
5. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can use, modify, and distribute this software freely, even for commercial purposes.

## Acknowledgments

- Built with ❤️ using Python
- Inspired by the simplicity of command-line productivity tools
- Created with Claude Code

---

**Star this repository** ⭐ if you find it helpful!

**Report issues** 🐛 on our [GitHub Issues page](https://github.com/suztat/Introduction_claude/issues)
