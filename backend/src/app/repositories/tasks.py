from abc import ABC, abstractmethod

from app.schemas.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def add_task(self, task: Task) -> Task:
        """
        This method creates a new task in the repository and throws an exception if something is wrong with input data.

        Args:
            task (Task): Task object with null id (it will be replaced if presented).

        Raises:
            ConstraintViolationError: If something wrong with input data (e.g. not-existing owner_id).

        Returns:
            Task: The new Task object with repository-given ID.
        """
        pass

    @abstractmethod
    def update_task(self, updated_task: Task) -> None:
        """
        Updates the task in the repository and throws an exception if the task's ID does not exist.

        Args:
            updated_task (Task): Task object with an ID that exists in the repository.
                                 The properties of this object will replace the corresponding
                                 properties in the repository's record.

        Raises:
             NotFoundError: If the ID of the given task does not exist in the repository.
        """
        pass

    @abstractmethod
    def delete_task_by_id(self, task_id: str) -> None:
        """
        Deletes the task with the specified task_id from the repository.
        Raises an exception if the task with the given ID is not found in the repository.

        Args:
            task_id (str): The task`s ID. Must exist in the repository.

        Raises:
            NotFoundError: If task with given task_id does not exist in the repository.
        """
        pass

    @abstractmethod
    def get_tasks_by_owner_id(self, owner_id: str) -> list[Task]:
        """
        Retrieves all tasks associated with the user specified by owner_id.
        Raises an exception if the user with the given ID is not found in the repository.

        Args:
            owner_id (str): The ID of the user who owns the tasks. Must exist in the repository.

        Raises:
            NotFoundError: If the user with the given owner_id does not exist in the repository.

        Returns:
            list[Task]: A list of Task objects owned by the user with the specified owner_id.
        """
        pass
