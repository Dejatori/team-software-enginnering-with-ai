import pytest
import os
import tempfile
from tasks import TaskManager


@pytest.fixture
def task_manager():
    """Create a fresh TaskManager instance for each test."""
    return TaskManager()


def test_add_task_basic(task_manager):
    """Test basic task addition functionality."""
    result = task_manager.add_task("Test task", priority=1)

    assert result["status"] == "success"
    assert result["task_id"] == 1

    tasks = task_manager.list_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Test task"
    assert tasks[0]["priority"] == 1


@pytest.mark.parametrize(
    "invalid_input, expected_message",
    [
        (None, "Task must be a string"),
        ("", "Task cannot be empty"),
        ("   ", "Task cannot be empty"),
    ],
)
def test_add_task_validation(task_manager, invalid_input, expected_message):
    """Test input validation for add_task method."""
    result = task_manager.add_task(invalid_input)

    assert result["status"] == "error"
    assert result["message"] == expected_message


def test_add_duplicate_task(task_manager):
    """Test handling of duplicate tasks."""
    task_manager.add_task("Duplicate task")
    result = task_manager.add_task("Duplicate task")

    assert result["status"] == "error"
    assert "already exists" in result["message"]


def test_remove_task(task_manager):
    """Test task removal functionality."""
    task_manager.add_task("Task to remove")
    result = task_manager.remove_task(1)

    assert result["status"] == "success"
    assert len(task_manager.list_tasks()) == 0


def test_remove_nonexistent_task(task_manager):
    """Test removing a task that doesn't exist."""
    result = task_manager.remove_task(999)

    assert result["status"] == "error"
    assert "not found" in result["message"]


def test_complete_task(task_manager):
    """Test marking a task as complete."""
    task_manager.add_task("Task to complete")
    result = task_manager.complete_task(1)

    assert result["status"] == "success"

    # Task should not appear in a default list
    tasks = task_manager.list_tasks()
    assert len(tasks) == 0

    # But should appear when show_completed is True
    tasks = task_manager.list_tasks(show_completed=True)
    assert len(tasks) == 1
    assert tasks[0]["completed"] is True


def test_complete_nonexistent_task(task_manager):
    """Test completing a task that doesn't exist."""
    result = task_manager.complete_task(999)

    assert result["status"] == "error"
    assert "not found" in result["message"]


def test_edit_task_description_only(task_manager):
    """Test editing only task description."""
    task_manager.add_task("Original description", priority=1)

    result = task_manager.edit_task(1, new_description="Updated description")
    assert result["status"] == "success"

    tasks = task_manager.list_tasks()
    assert tasks[0]["description"] == "Updated description"
    assert tasks[0]["priority"] == 1  # Unchanged


def test_edit_task_priority_only(task_manager):
    """Test editing only task priority."""
    task_manager.add_task("Original description", priority=1)

    result = task_manager.edit_task(1, new_priority=5)
    assert result["status"] == "success"

    tasks = task_manager.list_tasks()
    assert tasks[0]["description"] == "Original description"  # Unchanged
    assert tasks[0]["priority"] == 5


def test_edit_task_both_fields(task_manager):
    """Test editing both description and priority."""
    task_manager.add_task("Original description", priority=1)

    result = task_manager.edit_task(1, new_description="Both updated", new_priority=10)
    assert result["status"] == "success"

    tasks = task_manager.list_tasks()
    assert tasks[0]["description"] == "Both updated"
    assert tasks[0]["priority"] == 10


@pytest.mark.parametrize(
    "description, expected_status",
    [
        ("", "error"),
        ("   ", "error"),
    ],
)
def test_edit_task_invalid_description(task_manager, description, expected_status):
    """Test validation for invalid descriptions in edit_task."""
    task_manager.add_task("Task to edit")

    result = task_manager.edit_task(1, new_description=description)
    assert result["status"] == expected_status


def test_edit_task_none_description(task_manager):
    """Test that None description means 'don't change' in edit_task."""
    task_manager.add_task("Original task")

    # None means "don't change the description"
    result = task_manager.edit_task(1, new_description=None, new_priority=2)
    assert result["status"] == "success"

    tasks = task_manager.list_tasks()
    assert tasks[0]["description"] == "Original task"  # Should be unchanged
    assert tasks[0]["priority"] == 2  # Should be updated


def test_edit_nonexistent_task(task_manager):
    """Test editing a task that doesn't exist."""
    result = task_manager.edit_task(999, new_description="Won't work")

    assert result["status"] == "error"
    assert "not found" in result["message"]


def test_list_tasks_default_sorting(task_manager):
    """Test default sorting (by ID) in list_tasks."""
    task_manager.add_task("Low priority", priority=1)
    task_manager.add_task("High priority", priority=5)
    task_manager.add_task("Medium priority", priority=3)

    tasks = task_manager.list_tasks()

    assert len(tasks) == 3
    assert tasks[0]["description"] == "Low priority"
    assert tasks[1]["description"] == "High priority"
    assert tasks[2]["description"] == "Medium priority"


def test_list_tasks_priority_sorting(task_manager):
    """Test sorting by priority in list_tasks."""
    task_manager.add_task("Low priority", priority=1)
    task_manager.add_task("High priority", priority=5)
    task_manager.add_task("Medium priority", priority=3)

    tasks = task_manager.list_tasks(sort_by="priority")

    assert len(tasks) == 3
    assert tasks[0]["description"] == "High priority"
    assert tasks[1]["description"] == "Medium priority"
    assert tasks[2]["description"] == "Low priority"


def test_list_tasks_completed_filter(task_manager):
    """Test filtering completed tasks in list_tasks."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.complete_task(1)

    # Default should only show incomplete tasks
    tasks = task_manager.list_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Task 2"

    # Show all tasks including completed
    tasks = task_manager.list_tasks(show_completed=True)
    assert len(tasks) == 2


def test_clear_tasks(task_manager):
    """Test clearing all tasks."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")

    result = task_manager.clear_tasks()
    assert result["status"] == "success"
    assert len(task_manager.list_tasks()) == 0


def test_persistence_save_and_load():
    """Test saving and loading tasks from a file."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name

    try:
        # Add some tasks and save them
        manager1 = TaskManager()
        manager1.add_task("Task 1", priority=3)
        manager1.add_task("Task 2", priority=5)
        manager1.complete_task(1)

        result = manager1.save_to_file(temp_filename)
        assert result["status"] == "success"

        # Create a new task manager and load the tasks
        manager2 = TaskManager()
        result = manager2.load_from_file(temp_filename)
        assert result["status"] == "success"

        # Verify tasks were loaded correctly
        tasks = manager2.list_tasks(show_completed=True)
        assert len(tasks) == 2

        # Find tasks by ID
        task1 = next(t for t in tasks if t["id"] == 1)
        task2 = next(t for t in tasks if t["id"] == 2)

        # Check task details
        assert task1["description"] == "Task 1"
        assert task1["priority"] == 3
        assert task1["completed"] is True

        assert task2["description"] == "Task 2"
        assert task2["priority"] == 5
        assert task2["completed"] is False

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_persistence_load_nonexistent_file(task_manager):
    """Test loading from a non-existent file."""
    result = task_manager.load_from_file("nonexistent_file.json")

    assert result["status"] == "error"


def test_persistence_save_to_invalid_path(task_manager):
    """Test saving to an invalid file path."""
    result = task_manager.save_to_file("/invalid/path/file.json")

    assert result["status"] == "error"


def test_task_id_after_removal(task_manager):
    """Test that task IDs don't get reused after removal."""
    task_manager.add_task("Task 1")  # ID: 1
    task_manager.add_task("Task 2")  # ID: 2
    task_manager.remove_task(1)
    task_manager.add_task("Task 3")  # Should be ID: 3, not 1

    tasks = task_manager.list_tasks()
    assert len(tasks) == 2
    assert tasks[0]["id"] == 2
    assert tasks[1]["id"] == 3  # ID should be 3, not reusing 1


def test_invalid_sort_parameter(task_manager):
    """Test behavior with invalid sort parameter."""
    task_manager.add_task("Task 1")

    # Should default to ID sorting when invalid parameter is provided
    tasks = task_manager.list_tasks(sort_by="invalid_param")
    assert len(tasks) == 1
    assert tasks[0]["id"] == 1


def test_add_task_with_negative_priority(task_manager):
    """Test adding a task with negative priority."""
    result = task_manager.add_task("Negative priority task", priority=-5)

    # Current implementation allows negative priorities
    assert result["status"] == "success"
    tasks = task_manager.list_tasks()
    assert tasks[0]["priority"] == -5


def test_unicode_task_description(task_manager):
    """Test adding a task with Unicode characters."""
    description = "Unicode: こんにちは 你好 مرحبا"
    result = task_manager.add_task(description)

    assert result["status"] == "success"
    tasks = task_manager.list_tasks()
    assert tasks[0]["description"] == description


def test_file_format_corruption():
    """Test loading from a corrupted JSON file."""
    # Create a temporary file with invalid JSON content
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        temp_file.write("This is not valid JSON")
        temp_filename = temp_file.name

    try:
        manager = TaskManager()
        result = manager.load_from_file(temp_filename)

        assert result["status"] == "error"
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_empty_taskmanager_operations(task_manager):
    """Test operations on an empty TaskManager."""
    # List tasks on empty manager
    tasks = task_manager.list_tasks()
    assert len(tasks) == 0

    # Clear empty task list
    result = task_manager.clear_tasks()
    assert result["status"] == "success"
    assert result["message"] == "Cleared 0 tasks"

    # Remove non-existent task
    result = task_manager.remove_task(1)
    assert result["status"] == "error"


if __name__ == "__main__":
    pytest.main(["-v"])
