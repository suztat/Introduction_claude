"""
Unit tests for Task Automation CLI
"""

import os
import json
import pytest
import tempfile
from pathlib import Path
import sys

# Add parent directory to path to import task_cli
sys.path.insert(0, str(Path(__file__).parent.parent))

from task_cli import TaskManager, format_task


@pytest.fixture
def temp_task_file():
    """Create a temporary task file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    yield temp_file
    # Cleanup
    if os.path.exists(temp_file):
        os.remove(temp_file)


@pytest.fixture
def task_manager(temp_task_file):
    """Create a TaskManager instance with temporary file"""
    return TaskManager(data_file=temp_task_file)


class TestTaskManager:
    """Test cases for TaskManager class"""

    def test_initialization(self, task_manager):
        """Test TaskManager initialization"""
        assert task_manager.tasks == []
        assert isinstance(task_manager.tasks, list)

    def test_add_task(self, task_manager):
        """Test adding a new task"""
        task = task_manager.add_task("Test task", priority="high")

        assert task["id"] == 1
        assert task["description"] == "Test task"
        assert task["priority"] == "high"
        assert task["completed"] is False
        assert task["created_at"] is not None
        assert task["completed_at"] is None

    def test_add_multiple_tasks(self, task_manager):
        """Test adding multiple tasks"""
        task1 = task_manager.add_task("Task 1")
        task2 = task_manager.add_task("Task 2")
        task3 = task_manager.add_task("Task 3")

        assert task1["id"] == 1
        assert task2["id"] == 2
        assert task3["id"] == 3
        assert len(task_manager.tasks) == 3

    def test_list_tasks_empty(self, task_manager):
        """Test listing tasks when there are none"""
        tasks = task_manager.list_tasks()
        assert tasks == []

    def test_list_active_tasks(self, task_manager):
        """Test listing only active tasks"""
        task_manager.add_task("Active task 1")
        task_manager.add_task("Active task 2")
        task_manager.add_task("To be completed")

        # Complete one task
        task_manager.complete_task(3)

        active_tasks = task_manager.list_tasks(show_completed=False)
        assert len(active_tasks) == 2
        assert all(not task["completed"] for task in active_tasks)

    def test_list_all_tasks(self, task_manager):
        """Test listing all tasks including completed"""
        task_manager.add_task("Task 1")
        task_manager.add_task("Task 2")
        task_manager.complete_task(1)

        all_tasks = task_manager.list_tasks(show_completed=True)
        assert len(all_tasks) == 2

    def test_complete_task(self, task_manager):
        """Test completing a task"""
        task_manager.add_task("Task to complete")
        completed_task = task_manager.complete_task(1)

        assert completed_task is not None
        assert completed_task["completed"] is True
        assert completed_task["completed_at"] is not None

    def test_complete_nonexistent_task(self, task_manager):
        """Test completing a task that doesn't exist"""
        result = task_manager.complete_task(999)
        assert result is None

    def test_delete_task(self, task_manager):
        """Test deleting a task"""
        task_manager.add_task("Task to delete")
        task_manager.add_task("Task to keep")

        result = task_manager.delete_task(1)
        assert result is True
        assert len(task_manager.tasks) == 1
        assert task_manager.tasks[0]["id"] == 2

    def test_delete_nonexistent_task(self, task_manager):
        """Test deleting a task that doesn't exist"""
        result = task_manager.delete_task(999)
        assert result is False

    def test_persistence(self, temp_task_file):
        """Test that tasks are persisted to file"""
        # Create manager and add tasks
        manager1 = TaskManager(data_file=temp_task_file)
        manager1.add_task("Persistent task 1")
        manager1.add_task("Persistent task 2")

        # Create new manager with same file
        manager2 = TaskManager(data_file=temp_task_file)

        assert len(manager2.tasks) == 2
        assert manager2.tasks[0]["description"] == "Persistent task 1"
        assert manager2.tasks[1]["description"] == "Persistent task 2"

    def test_task_priorities(self, task_manager):
        """Test different priority levels"""
        high_task = task_manager.add_task("High priority", priority="high")
        medium_task = task_manager.add_task("Medium priority", priority="medium")
        low_task = task_manager.add_task("Low priority", priority="low")

        assert high_task["priority"] == "high"
        assert medium_task["priority"] == "medium"
        assert low_task["priority"] == "low"


class TestFormatTask:
    """Test cases for format_task function"""

    def test_format_active_task(self):
        """Test formatting an active task"""
        task = {
            "id": 1,
            "description": "Test task",
            "priority": "medium",
            "completed": False
        }
        formatted = format_task(task)
        assert "[1]" in formatted
        assert "○" in formatted
        assert "🟡" in formatted
        assert "Test task" in formatted

    def test_format_completed_task(self):
        """Test formatting a completed task"""
        task = {
            "id": 2,
            "description": "Completed task",
            "priority": "high",
            "completed": True
        }
        formatted = format_task(task)
        assert "[2]" in formatted
        assert "✓" in formatted
        assert "🔴" in formatted
        assert "Completed task" in formatted

    def test_format_task_all_priorities(self):
        """Test formatting tasks with different priorities"""
        high_task = {"id": 1, "description": "High", "priority": "high", "completed": False}
        medium_task = {"id": 2, "description": "Medium", "priority": "medium", "completed": False}
        low_task = {"id": 3, "description": "Low", "priority": "low", "completed": False}

        assert "🔴" in format_task(high_task)
        assert "🟡" in format_task(medium_task)
        assert "🟢" in format_task(low_task)


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_load_corrupted_json(self, temp_task_file):
        """Test loading from corrupted JSON file"""
        # Write invalid JSON
        with open(temp_task_file, 'w') as f:
            f.write("invalid json content {{{")

        manager = TaskManager(data_file=temp_task_file)
        assert manager.tasks == []

    def test_empty_task_description(self, task_manager):
        """Test adding task with empty description"""
        task = task_manager.add_task("")
        assert task["description"] == ""

    def test_special_characters_in_description(self, task_manager):
        """Test task with special characters"""
        description = "Task with émojis 🎉 and spëcial çhars"
        task = task_manager.add_task(description)
        assert task["description"] == description


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
