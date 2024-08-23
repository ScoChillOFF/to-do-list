from abc import ABC, abstractmethod

from app.schemas.task import Task
from app.schemas.user import User


class TaskService(ABC):
    @abstractmethod
    def add_task(self, task: Task) -> Task:
        """
        Adds the given Task object to the repository. Throws an exception if the owner of the task does not exist

        Args:
            task (Task): The Task object to be added. The object should contain a valid owner_id.

        Raises:
            UserNotFoundError: If the owner id specified in the task does not exist in the repository.

        Returns:
            Task: The Task object with the repository-generated ID.
        """
        pass

    @abstractmethod
    def change_complete_status(self, task: Task) -> None:
        """
        Changes the given task`s complete status to opposite.
        Throws an exception when the task does not exist in repository.

        Args:
            task (Task): Task to be updated.

        Raises:
            TaskNotFoundError: When the task does not exist in the repository.
        """
        pass

    @abstractmethod
    def get_user_tasks(self, user: User) -> list[Task]:
        """
        Retrieves all the tasks that belong to the given user.
        Returns an empty list if the user does not exist in the repository.

        Args:
            user (User)

        Returns:
            list[Task]: The user`s tasks.
        """

    @abstractmethod
    def delete_task(self, task: Task) -> None:
        """
       Deletes the specified task from the repository. Throws an exception if the task does not exist.

       Args:
           task (Task): The Task object to be deleted.

       Raises:
           TaskNotFoundError: If the task with the given ID does not exist in the repository.
       """
        pass
