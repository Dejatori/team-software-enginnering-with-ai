import unittest
import os
import tempfile
from tasks import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        """Set up a fresh TaskManager instance before each test."""
        self.task_manager = TaskManager()

    def test_add_task_basic(self):
        """Test basic task addition functionality."""
        result = self.task_manager.add_task("Test task", priority=1)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["task_id"], 1)

        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Test task")
        self.assertEqual(tasks[0]["priority"], 1)

    def test_add_task_validation(self):
        """Test input validation for add_task method."""
        # Test None input
        result = self.task_manager.add_task(None)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Task must be a string")

        # Test empty string
        result = self.task_manager.add_task("")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Task cannot be empty")

        # Test whitespace-only string
        result = self.task_manager.add_task("   ")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Task cannot be empty")

    def test_add_duplicate_task(self):
        """Test handling of duplicate tasks."""
        self.task_manager.add_task("Duplicate task")
        result = self.task_manager.add_task("Duplicate task")
        self.assertEqual(result["status"], "error")
        self.assertTrue("already exists" in result["message"])

    def test_remove_task(self):
        """Test task removal functionality."""
        self.task_manager.add_task("Task to remove")
        result = self.task_manager.remove_task(1)
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(self.task_manager.list_tasks()), 0)

    def test_remove_nonexistent_task(self):
        """Test removing a task that doesn't exist."""
        result = self.task_manager.remove_task(999)
        self.assertEqual(result["status"], "error")
        self.assertTrue("not found" in result["message"])

    def test_complete_task(self):
        """Test marking a task as complete."""
        self.task_manager.add_task("Task to complete")
        result = self.task_manager.complete_task(1)
        self.assertEqual(result["status"], "success")

        # Task should not appear in a default list
        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 0)

        # But should appear when show_completed is True
        tasks = self.task_manager.list_tasks(show_completed=True)
        self.assertEqual(len(tasks), 1)
        self.assertTrue(tasks[0]["completed"])

    def test_complete_nonexistent_task(self):
        """Test completing a task that doesn't exist."""
        result = self.task_manager.complete_task(999)
        self.assertEqual(result["status"], "error")
        self.assertTrue("not found" in result["message"])

    def test_edit_task(self):
        """Test editing task description and priority."""
        self.task_manager.add_task("Original description", priority=1)

        # Edit description only
        result = self.task_manager.edit_task(1, new_description="Updated description")
        self.assertEqual(result["status"], "success")
        tasks = self.task_manager.list_tasks()
        self.assertEqual(tasks[0]["description"], "Updated description")
        self.assertEqual(tasks[0]["priority"], 1)  # Unchanged

        # Edit priority only
        result = self.task_manager.edit_task(1, new_priority=5)
        self.assertEqual(result["status"], "success")
        tasks = self.task_manager.list_tasks()
        self.assertEqual(tasks[0]["description"], "Updated description")  # Unchanged
        self.assertEqual(tasks[0]["priority"], 5)

        # Edit both
        result = self.task_manager.edit_task(
            1, new_description="Both updated", new_priority=10
        )
        self.assertEqual(result["status"], "success")
        tasks = self.task_manager.list_tasks()
        self.assertEqual(tasks[0]["description"], "Both updated")
        self.assertEqual(tasks[0]["priority"], 10)

    def test_edit_task_validation(self):
        """Test validation in edit_task method."""
        self.task_manager.add_task("Task to edit")

        # Test empty description
        result = self.task_manager.edit_task(1, new_description="")
        self.assertEqual(result["status"], "error")

        # Test whitespace-only description
        result = self.task_manager.edit_task(1, new_description="   ")
        self.assertEqual(result["status"], "error")

        # Test non-string description - passing None actually means "don't change description"
        # so it should succeed if a task exists and only priority is changed
        result = self.task_manager.edit_task(1, new_description=None, new_priority=2)
        self.assertEqual(result["status"], "success")

    def test_edit_nonexistent_task(self):
        """Test editing a task that doesn't exist."""
        result = self.task_manager.edit_task(999, new_description="Won't work")
        self.assertEqual(result["status"], "error")
        self.assertTrue("not found" in result["message"])

    def test_list_tasks_sorting(self):
        """Test task listing with different sorting options."""
        # Add tasks with different priorities
        self.task_manager.add_task("Low priority", priority=1)
        self.task_manager.add_task("High priority", priority=5)
        self.task_manager.add_task("Medium priority", priority=3)

        # Test default sorting (by ID)
        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0]["description"], "Low priority")
        self.assertEqual(tasks[1]["description"], "High priority")
        self.assertEqual(tasks[2]["description"], "Medium priority")

        # Test priority sorting
        tasks = self.task_manager.list_tasks(sort_by="priority")
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0]["description"], "High priority")
        self.assertEqual(tasks[1]["description"], "Medium priority")
        self.assertEqual(tasks[2]["description"], "Low priority")

    def test_list_tasks_completed_filter(self):
        """Test filtering completed tasks."""
        self.task_manager.add_task("Task 1")
        self.task_manager.add_task("Task 2")
        self.task_manager.complete_task(1)

        # Default should only show incomplete tasks
        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Task 2")

        # Show all tasks
        tasks = self.task_manager.list_tasks(show_completed=True)
        self.assertEqual(len(tasks), 2)

    def test_clear_tasks(self):
        """Test clearing all tasks."""
        self.task_manager.add_task("Task 1")
        self.task_manager.add_task("Task 2")

        result = self.task_manager.clear_tasks()
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(self.task_manager.list_tasks()), 0)

    def test_persistence(self):
        """Test saving and loading tasks."""
        # Create a temporary file
        temp_fd, temp_filename = tempfile.mkstemp()
        os.close(temp_fd)

        try:
            # Add some tasks and save them
            self.task_manager.add_task("Task 1", priority=3)
            self.task_manager.add_task("Task 2", priority=5)
            self.task_manager.complete_task(1)

            result = self.task_manager.save_to_file(temp_filename)
            self.assertEqual(result["status"], "success")

            # Create a new task manager and load the tasks
            new_manager = TaskManager()
            result = new_manager.load_from_file(temp_filename)
            self.assertEqual(result["status"], "success")

            # Verify tasks were loaded correctly
            tasks = new_manager.list_tasks(show_completed=True)
            self.assertEqual(len(tasks), 2)

            # Check specific task details
            task1 = next(t for t in tasks if t["id"] == 1)
            self.assertEqual(task1["description"], "Task 1")
            self.assertEqual(task1["priority"], 3)
            self.assertTrue(task1["completed"])

            task2 = next(t for t in tasks if t["id"] == 2)
            self.assertEqual(task2["description"], "Task 2")
            self.assertEqual(task2["priority"], 5)
            self.assertFalse(task2["completed"])

        finally:
            # Clean up the temporary file
            os.remove(temp_filename)

    def test_persistence_error_handling(self):
        """Test error handling in file operations."""
        # Test loading from a non-existent file
        result = self.task_manager.load_from_file("nonexistent_file.json")
        self.assertEqual(result["status"], "error")

        # Test saving to a invalid path
        result = self.task_manager.save_to_file("/invalid/path/file.json")
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
