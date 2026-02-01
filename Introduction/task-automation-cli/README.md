# Task Automation CLI

A simple, lightweight command-line task management tool written in Python.

## Features

- ✅ Add tasks with priorities (low, medium, high)
- 📋 List active and completed tasks
- ✓ Mark tasks as completed
- 🗑️ Delete tasks
- 💾 Store tasks in JSON format
- 🎨 Color-coded priority indicators

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd task-automation-cli
```

2. (Optional) Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make the script executable:
```bash
chmod +x task_cli.py
```

## Usage

### Add a new task

```bash
python task_cli.py add "Finish project documentation"
python task_cli.py add "Review pull requests" -p high
python task_cli.py add "Update dependencies" --priority low
```

### List tasks

```bash
# List active tasks only
python task_cli.py list

# List all tasks (including completed)
python task_cli.py list --all
python task_cli.py list -a
```

### Complete a task

```bash
python task_cli.py complete 1
```

### Delete a task

```bash
python task_cli.py delete 2
```

## Examples

```bash
# Add some tasks
$ python task_cli.py add "Write unit tests" -p high
✓ Task added: [1] ○ 🔴 Write unit tests

$ python task_cli.py add "Update README" -p medium
✓ Task added: [2] ○ 🟡 Update README

$ python task_cli.py add "Refactor code" -p low
✓ Task added: [3] ○ 🟢 Refactor code

# List active tasks
$ python task_cli.py list

Active Tasks:
--------------------------------------------------
[1] ○ 🔴 Write unit tests
[2] ○ 🟡 Update README
[3] ○ 🟢 Refactor code
--------------------------------------------------
Total: 3 task(s)

# Complete a task
$ python task_cli.py complete 1
✓ Task completed: [1] ✓ 🔴 Write unit tests

# List with completed tasks
$ python task_cli.py list -a

All Tasks:
--------------------------------------------------
[1] ✓ 🔴 Write unit tests
[2] ○ 🟡 Update README
[3] ○ 🟢 Refactor code
--------------------------------------------------
Total: 3 task(s)
```

## Data Storage

Tasks are stored in a `tasks.json` file in the current working directory. The file is automatically created when you add your first task.

## Priority Levels

- 🔴 **High**: Urgent and important tasks
- 🟡 **Medium**: Normal priority tasks (default)
- 🟢 **Low**: Nice-to-have tasks

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Run tests with coverage:

```bash
python -m pytest --cov=task_cli tests/
```

## Development

### Project Structure

```
task-automation-cli/
├── task_cli.py          # Main CLI application
├── tests/               # Test files
│   └── test_task_cli.py
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - feel free to use this project for any purpose.

## Author

Created with ❤️ by the development team
