library(R6)
library(jsonlite)

TaskManager <- R6Class("TaskManager",
  private = list(
    tasks = list(),
    next_id = 1
  ),

  public = list(
    initialize = function() {
      # Initialize empty task list
      private$tasks <- list()
      private$next_id <- 1
    },

    add_task = function(task, priority = 0) {
      # Validate task
      if (is.null(task) || !is.character(task)) {
        return(list(status = "error", message = "Task must be a string"))
      }

      if (trimws(task) == "") {
        return(list(status = "error", message = "Task cannot be empty"))
      }

      # Check for duplicates
      task_descriptions <- sapply(private$tasks, function(t) t$description)
      if (task %in% task_descriptions) {
        return(list(status = "error", message = sprintf("Task '%s' already exists", task)))
      }

      # Create task object
      task_obj <- list(
        description = task,
        priority = priority,
        completed = FALSE,
        id = private$next_id
      )

      private$next_id <- private$next_id + 1
      private$tasks <- c(private$tasks, list(task_obj))

      return(list(
        status = "success",
        message = sprintf("Task '%s' added", task),
        task_id = task_obj$id
      ))
    },

    remove_task = function(task_id) {
      for (i in seq_along(private$tasks)) {
        if (private$tasks[[i]]$id == task_id) {
          removed <- private$tasks[[i]]
          private$tasks <- private$tasks[-i]
          return(list(
            status = "success",
            message = sprintf("Task '%s' removed", removed$description)
          ))
        }
      }

      return(list(
        status = "error",
        message = sprintf("Task with ID %d not found", task_id)
      ))
    },

    complete_task = function(task_id) {
      for (i in seq_along(private$tasks)) {
        if (private$tasks[[i]]$id == task_id) {
          private$tasks[[i]]$completed <- TRUE
          return(list(
            status = "success",
            message = sprintf("Completed task: '%s'", private$tasks[[i]]$description)
          ))
        }
      }

      return(list(
        status = "error",
        message = sprintf("Task with ID %d not found", task_id)
      ))
    },

    edit_task = function(task_id, new_description = NULL, new_priority = NULL) {
      for (i in seq_along(private$tasks)) {
        if (private$tasks[[i]]$id == task_id) {
          if (!is.null(new_description)) {
            if (!is.character(new_description) || trimws(new_description) == "") {
              return(list(
                status = "error",
                message = "New description must be a non-empty string"
              ))
            }
            private$tasks[[i]]$description <- new_description
          }

          if (!is.null(new_priority)) {
            private$tasks[[i]]$priority <- new_priority
          }

          return(list(
            status = "success",
            message = sprintf("Task %d updated", task_id)
          ))
        }
      }

      return(list(
        status = "error",
        message = sprintf("Task with ID %d not found", task_id)
      ))
    },

    list_tasks = function(sort_by = "id", show_completed = FALSE) {
      # Filter completed tasks if needed
      tasks_to_show <- private$tasks
      if (!show_completed) {
        tasks_to_show <- Filter(function(t) !t$completed, tasks_to_show)
      }

      # Sort tasks
      if (length(tasks_to_show) == 0) {
        return(list())
      }

      if (sort_by == "priority") {
        # Sort by priority (descending)
        task_priorities <- sapply(tasks_to_show, function(t) t$priority)
        tasks_to_show <- tasks_to_show[order(task_priorities, decreasing = TRUE)]
      } else {
        # Sort by id (ascending)
        task_ids <- sapply(tasks_to_show, function(t) t$id)
        tasks_to_show <- tasks_to_show[order(task_ids)]
      }

      return(tasks_to_show)
    },

    clear_tasks = function() {
      task_count <- length(private$tasks)
      private$tasks <- list()

      return(list(
        status = "success",
        message = sprintf("Cleared %d tasks", task_count)
      ))
    },

    save_to_file = function(filename) {
      tryCatch({
        write_json(private$tasks, filename)
        return(list(
          status = "success",
          message = sprintf("Saved %d tasks to %s", length(private$tasks), filename)
        ))
      }, error = function(e) {
        return(list(
          status = "error",
          message = sprintf("Failed to save tasks: %s", e$message)
        ))
      })
    },

    load_from_file = function(filename) {
      tryCatch({
        private$tasks <- read_json(filename)
        return(list(
          status = "success",
          message = sprintf("Loaded %d tasks from %s", length(private$tasks), filename)
        ))
      }, error = function(e) {
        return(list(
          status = "error",
          message = sprintf("Failed to load tasks: %s", e$message)
        ))
      })
    }
  )
)

# Example usage
if (interactive()) {
  task_mgr <- TaskManager$new()

  print(task_mgr$add_task("Buy groceries", priority = 2))
  print(task_mgr$add_task("Read a book", priority = 1))
  print(task_mgr$add_task(""))  # Will be rejected
  print(task_mgr$add_task(NULL))  # Will be rejected

  cat("\nTasks sorted by ID:\n")
  print(task_mgr$list_tasks())

  cat("\nTasks sorted by priority:\n")
  print(task_mgr$list_tasks(sort_by = "priority"))

  cat("\nCompleting and editing tasks:\n")
  print(task_mgr$complete_task(1))
  print(task_mgr$edit_task(2, new_description = "Read R book", new_priority = 3))

  cat("\nAfter edits (including completed):\n")
  print(task_mgr$list_tasks(show_completed = TRUE))
}