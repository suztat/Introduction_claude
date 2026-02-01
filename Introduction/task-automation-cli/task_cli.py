#!/usr/bin/env python3
"""
Task Automation CLI - A simple command-line task management tool
"""

import json
import os
import argparse
from datetime import datetime
from typing import List, Dict, Optional


class TaskManager:
    """Manages tasks stored in a JSON file"""

    def __init__(self, data_file: str = "tasks.json"):
        """Initialize TaskManager with a data file path"""
        self.data_file = data_file
        self.tasks: List[Dict] = self._load_tasks()

    def _load_tasks(self) -> List[Dict]:
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_tasks(self) -> None:
        """Save tasks to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)

    def add_task(self, description: str, priority: str = "medium") -> Dict:
        """Add a new task"""
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
        """List all tasks or only active tasks"""
        if show_completed:
            return self.tasks
        return [task for task in self.tasks if not task["completed"]]

    def complete_task(self, task_id: int) -> Optional[Dict]:
        """Mark a task as completed"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self._save_tasks()
                return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID"""
        initial_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        if len(self.tasks) < initial_length:
            self._save_tasks()
            return True
        return False


def format_task(task: Dict) -> str:
    """Format a task for display"""
    status = "✓" if task["completed"] else "○"
    priority_symbols = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }
    priority = priority_symbols.get(task["priority"], "⚪")
    return f"[{task['id']}] {status} {priority} {task['description']}"


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Task Automation CLI - Manage your tasks from the command line"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument(
        "-p", "--priority",
        choices=["low", "medium", "high"],
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
