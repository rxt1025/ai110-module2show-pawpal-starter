"""PawPal+ core system.

Models an owner, their pets, and the pet-care tasks for each pet.
The Scheduler is the "brain" that retrieves, organizes, and manages
tasks across all of an owner's pets.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet-care activity."""

    description: str          # what needs to happen, e.g. "Morning walk"
    time: str                 # when it happens, e.g. "08:00"
    frequency: str            # how often, e.g. "daily" | "weekly"
    completed: bool = False   # completion status

    def mark_done(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_undone(self) -> None:
        """Mark this task as not yet completed."""
        self.completed = False


@dataclass
class Pet:
    """Stores a pet's details and its list of tasks."""

    name: str
    species: str                                  # "dog" | "cat" | "other"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The brain: retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    # --- Retrieve ---------------------------------------------------------

    def get_all_tasks(self) -> list[Task]:
        """Retrieve every task belonging to the owner's pets."""
        return self.owner.all_tasks()

    def pending_tasks(self) -> list[Task]:
        """Retrieve only the tasks that are not yet completed."""
        return [task for task in self.get_all_tasks() if not task.completed]

    def completed_tasks(self) -> list[Task]:
        """Retrieve only the tasks that have been completed."""
        return [task for task in self.get_all_tasks() if task.completed]

    # --- Organize ---------------------------------------------------------

    def daily_schedule(self) -> list[Task]:
        """Return all tasks ordered by their scheduled time of day."""
        return sorted(self.get_all_tasks(), key=lambda task: task.time)

    def tasks_by_frequency(self, frequency: str) -> list[Task]:
        """Return tasks matching a given frequency (e.g. 'daily')."""
        return [
            task for task in self.get_all_tasks()
            if task.frequency == frequency
        ]

    # --- Manage -----------------------------------------------------------

    def mark_complete(self, task: Task) -> None:
        """Mark a task as done."""
        task.mark_done()

    def progress_summary(self) -> str:
        """Return a short summary of how many tasks are done vs. remaining."""
        all_tasks = self.get_all_tasks()
        done = len(self.completed_tasks())
        return f"{done} of {len(all_tasks)} tasks completed."
