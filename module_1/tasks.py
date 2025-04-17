class TaskManager:
    def __init__(self):
        """Initialize an empty task list."""
        self._tasks = []
        self._completed_tasks = []
        self._next_id = 1

    def add_task(self, task, priority=0):
        """
        Add a task with optional priority if valid.

        Args:
            task: Task description (string)
            priority: Task priority (integer), higher means more important

        Returns:
            dict: Status and message
        """
        if task is None or not isinstance(task, str):
            return {"status": "error", "message": "Task must be a string"}

        if not task.strip():
            return {"status": "error", "message": "Task cannot be empty"}

        if task in [t["description"] for t in self._tasks]:
            return {"status": "error", "message": f"Task '{task}' already exists"}

        # Add a task with metadata
        task_obj = {
            "description": task,
            "priority": priority,
            "completed": False,
            "id": self._next_id,
        }
        self._next_id += 1
        self._tasks.append(task_obj)
        return {
            "status": "success",
            "message": f"Task '{task}' added",
            "task_id": task_obj["id"],
        }

    def remove_task(self, task_id):
        """
        Remove a task by its ID.

        Returns:
            dict: Status and message
        """
        for i, task in enumerate(self._tasks):
            if task["id"] == task_id:
                removed = self._tasks.pop(i)
                return {
                    "status": "success",
                    "message": f"Task '{removed['description']}' removed",
                }

        return {"status": "error", "message": f"Task with ID {task_id} not found"}

    def complete_task(self, task_id):
        """Mark a task as completed."""
        for task in self._tasks:
            if task["id"] == task_id:
                task["completed"] = True
                return {
                    "status": "success",
                    "message": f"Completed task: '{task['description']}'",
                }

        return {"status": "error", "message": f"Task with ID {task_id} not found"}

    def edit_task(self, task_id, new_description=None, new_priority=None):
        """Edit an existing task's description or priority."""
        for task in self._tasks:
            if task["id"] == task_id:
                if new_description is not None:
                    if (
                        not isinstance(new_description, str)
                        or not new_description.strip()
                    ):
                        return {
                            "status": "error",
                            "message": "New description must be a non-empty string",
                        }
                    task["description"] = new_description

                if new_priority is not None:
                    task["priority"] = new_priority

                return {"status": "success", "message": f"Task {task_id} updated"}

        return {"status": "error", "message": f"Task with ID {task_id} not found"}

    def list_tasks(self, sort_by="id", show_completed=False):
        """
        List all tasks with optional sorting.

        Args:
            sort_by: Field to sort by ('id', 'priority')
            show_completed: Whether to include completed tasks

        Returns:
            list: Tasks matching criteria
        """
        tasks_to_show = self._tasks

        if not show_completed:
            tasks_to_show = [t for t in tasks_to_show if not t["completed"]]

        if sort_by == "priority":
            return sorted(tasks_to_show, key=lambda x: x["priority"], reverse=True)
        else:
            return sorted(tasks_to_show, key=lambda x: x["id"])

    def clear_tasks(self):
        """Remove all tasks."""
        task_count = len(self._tasks)
        self._tasks = []
        return {"status": "success", "message": f"Cleared {task_count} tasks"}

    def save_to_file(self, filename):
        """Save tasks to a file."""
        try:
            import json

            with open(filename, "w") as f:
                json.dump(self._tasks, f)
            return {
                "status": "success",
                "message": f"Saved {len(self._tasks)} tasks to {filename}",
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to save tasks: {str(e)}"}

    def load_from_file(self, filename):
        """Load tasks from a file."""
        try:
            import json

            with open(filename, "r") as f:
                self._tasks = json.load(f)
            return {
                "status": "success",
                "message": f"Loaded {len(self._tasks)} tasks from {filename}",
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to load tasks: {str(e)}"}


# Example usage
if __name__ == "__main__":
    task_mgr = TaskManager()

    print(task_mgr.add_task("Buy groceries", priority=2))
    print(task_mgr.add_task("Read a book", priority=1))
    print(task_mgr.add_task(""))  # Will be rejected
    print(task_mgr.add_task(None))  # Will be rejected

    print("\nTasks sorted by ID:")
    print(task_mgr.list_tasks())

    print("\nTasks sorted by priority:")
    print(task_mgr.list_tasks(sort_by="priority"))

    print("\nCompleting and editing tasks:")
    print(task_mgr.complete_task(1))
    print(task_mgr.edit_task(2, new_description="Read Python book", new_priority=3))

    print("\nAfter edits (including completed):")
    print(task_mgr.list_tasks(show_completed=True))
