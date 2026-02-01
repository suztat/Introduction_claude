#!/usr/bin/env python3
"""
Task Automation CLI - A simple command-line task management tool

This module provides a command-line interface for managing tasks with
priorities, completion tracking, and persistent JSON storage.

Example:
    $ python task_cli.py add "Complete documentation" -p high
    $ python task_cli.py list
    $ python task_cli.py complete 1

Author: Task Automation CLI Contributors
License: MIT
"""

import json
import os
import argparse
from datetime import datetime
from typing import List, Dict, Optional


class TaskManager:
    """
    Manages tasks with persistent JSON storage.

    This class handles task creation, retrieval, completion, and deletion,
    with automatic persistence to a JSON file.

    Attributes:
        data_file: Path to the JSON file for storing tasks
        tasks: List of task dictionaries

    Example:
        >>> manager = TaskManager("my_tasks.json")
        >>> task = manager.add_task("Buy groceries", priority="high")
        >>> tasks = manager.list_tasks()
    """

    def __init__(self, data_file: str = "tasks.json"):
        """
        Initialize TaskManager with a data file path.

        Args:
            data_file: Path to the JSON file for storing tasks.
                      Defaults to "tasks.json" in the current directory.

        Note:
            If the file doesn't exist, it will be created automatically
            when the first task is added.
        """
        self.data_file = data_file
        self.tasks: List[Dict] = self._load_tasks()

    def _load_tasks(self) -> List[Dict]:
        """
        Load tasks from JSON file.

        Returns:
            List of task dictionaries. Returns empty list if file doesn't
            exist or contains invalid JSON.

        Note:
            This is a private method called during initialization.
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_tasks(self) -> None:
        """
        Save tasks to JSON file.

        Writes the current tasks list to the JSON file with UTF-8 encoding
        and pretty-printing (2-space indentation).

        Note:
            This is a private method called after any task modification.
        """
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)

    def add_task(self, description: str, priority: str = "medium") -> Dict:
        """
        Add a new task with the specified description and priority.

        Args:
            description: The task description text
            priority: Priority level - one of "low", "medium", "high", or "urgent".
                     Defaults to "medium".

        Returns:
            Dictionary containing the created task with fields:
            - id: Unique task identifier
            - description: Task description
            - priority: Priority level
            - completed: Completion status (always False for new tasks)
            - created_at: ISO format timestamp of creation
            - completed_at: Completion timestamp (None for new tasks)

        Example:
            >>> task = manager.add_task("Write tests", priority="high")
            >>> print(task["id"])
            1
        """
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        self.tasks.append(task)
        self._save_tasks()
        return task

    def list_tasks(self, show_completed: bool = False) -> List[Dict]:
        """
        List tasks, optionally including completed ones.

        Args:
            show_completed: If True, return all tasks including completed.
                           If False (default), return only active tasks.

        Returns:
            List of task dictionaries matching the filter criteria.

        Example:
            >>> active_tasks = manager.list_tasks()
            >>> all_tasks = manager.list_tasks(show_completed=True)
        """
        if show_completed:
            return self.tasks
        return [task for task in self.tasks if not task["completed"]]

    def complete_task(self, task_id: int) -> Optional[Dict]:
        """
        Mark a task as completed and record the completion time.

        Args:
            task_id: The unique ID of the task to complete

        Returns:
            The completed task dictionary if found, None otherwise.
            The task will have its 'completed' field set to True and
            'completed_at' set to the current timestamp.

        Example:
            >>> task = manager.complete_task(1)
            >>> if task:
            ...     print(f"Completed: {task['description']}")
        """
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self._save_tasks()
                return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Permanently delete a task by its ID.

        Args:
            task_id: The unique ID of the task to delete

        Returns:
            True if the task was found and deleted, False otherwise.

        Warning:
            This operation is irreversible. The task will be permanently
            removed from the JSON file.

        Example:
            >>> if manager.delete_task(1):
            ...     print("Task deleted successfully")
            ... else:
            ...     print("Task not found")
        """
        initial_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        if len(self.tasks) < initial_length:
            self._save_tasks()
            return True
        return False


def format_task(task: Dict) -> str:
    """
    Format a task dictionary as a display string with status and priority.

    Args:
        task: Task dictionary containing 'id', 'description', 'priority',
              and 'completed' fields

    Returns:
        Formatted string in the format:
        "[ID] STATUS PRIORITY_SYMBOL Description"

        Status symbols:
        - ✓ for completed tasks
        - ○ for active tasks

        Priority symbols:
        - 🚨 for urgent priority
        - 🔴 for high priority
        - 🟡 for medium priority
        - 🟢 for low priority
        - ⚪ for unknown priority

    Example:
        >>> task = {"id": 1, "description": "Test", "priority": "high", "completed": False}
        >>> print(format_task(task))
        [1] ○ 🔴 Test
    """
    status = "✓" if task["completed"] else "○"
    priority_symbols = {
        "urgent": "🚨",
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }
    priority = priority_symbols.get(task["priority"], "⚪")
    return f"[{task['id']}] {status} {priority} {task['description']}"


def main():
    """
    Main CLI entry point - parse arguments and execute commands.

    This function sets up the argument parser with subcommands for:
    - add: Add a new task
    - list: List tasks
    - complete: Mark a task as completed
    - delete: Delete a task

    The function parses command-line arguments, initializes TaskManager,
    and executes the requested command.

    Example:
        $ python task_cli.py add "My task" -p high
        $ python task_cli.py list
        $ python task_cli.py complete 1
        $ python task_cli.py delete 2
    """
    parser = argparse.ArgumentParser(
        description="Task Automation CLI - Manage your tasks from the command line"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument(
        "-p", "--priority",
        choices=["low", "medium", "high", "urgent"],
        default="medium",
        help="Task priority (default: medium)"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Show completed tasks as well"
    )

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", type=int, help="Task ID to complete")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID to delete")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize TaskManager
    manager = TaskManager()

    # Execute commands
    if args.command == "add":
        task = manager.add_task(args.description, args.priority)
        print(f"✓ Task added: {format_task(task)}")

    elif args.command == "list":
        tasks = manager.list_tasks(show_completed=args.all)
        if not tasks:
            print("No tasks found.")
        else:
            print(f"\n{'All Tasks' if args.all else 'Active Tasks'}:")
            print("-" * 50)
            for task in tasks:
                print(format_task(task))
            print("-" * 50)
            print(f"Total: {len(tasks)} task(s)")

    elif args.command == "complete":
        task = manager.complete_task(args.task_id)
        if task:
            print(f"✓ Task completed: {format_task(task)}")
        else:
            print(f"✗ Task ID {args.task_id} not found.")

    elif args.command == "delete":
        if manager.delete_task(args.task_id):
            print(f"✓ Task {args.task_id} deleted.")
        else:
            print(f"✗ Task ID {args.task_id} not found.")


if __name__ == "__main__":
    main()
