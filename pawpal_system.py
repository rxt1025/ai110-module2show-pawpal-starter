"""PawPal+ core system.

Models an owner, their pets, and the pet-care tasks for each pet.
The Scheduler is the "brain" that retrieves, organizes, and manages
tasks across all of an owner's pets.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta

# How far ahead the next occurrence lands, per frequency.
_FREQUENCY_STEP = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
}


@dataclass
class Task:
    """A single pet-care activity."""

    description: str          # what needs to happen, e.g. "Morning walk"
    time: str                 # when it happens, e.g. "08:00"
    frequency: str            # how often, e.g. "daily" | "weekly"
    completed: bool = False   # completion status
    scheduled_date: date = field(default_factory=date.today)  # day it's scheduled for

    def mark_done(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_undone(self) -> None:
        """Mark this task as not yet completed."""
        self.completed = False

    def next_occurrence(self) -> "Task | None":
        """Build a fresh, uncompleted copy of this task for its next slot.

        Algorithm: look up the frequency's step in ``_FREQUENCY_STEP`` and
        add that ``timedelta`` to ``scheduled_date`` (daily -> +1 day,
        weekly -> +7 days). ``timedelta`` arithmetic rolls over months,
        years, and leap days automatically.

        Returns:
            A new ``Task`` on the next date with ``completed=False``, or
            ``None`` for one-off tasks (any frequency not in
            ``_FREQUENCY_STEP``), so callers can tell whether it repeats.
        """
        step = _FREQUENCY_STEP.get(self.frequency)
        if step is None:
            return None
        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            completed=False,
            scheduled_date=self.scheduled_date + step,
        )


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

    def sort_by_time(self) -> list[Task]:
        """Return all tasks ordered by their scheduled 'HH:MM' time.

        Algorithm: ``sorted()`` with a ``key`` lambda that reads each
        task's ``time`` string. Because times are zero-padded 'HH:MM',
        lexicographic string order matches chronological order (e.g.
        '07:30' < '08:00' < '18:00'). Runs in O(n log n) and returns a new
        list, leaving each pet's task list untouched.

        Returns:
            A new list of every task across all pets, earliest first.
        """
        return sorted(self.get_all_tasks(), key=lambda task: task.time)

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks that overlap in time.

        Lightweight strategy: bucket every pending task into a dict keyed
        by its ``(scheduled_date, time)`` slot in a single O(n) pass, then
        report any slot holding more than one task. This avoids comparing
        every task against every other (which would be O(n^2)). A conflict
        counts whether the clashing tasks belong to the same pet or to
        different pets. Completed tasks are skipped since a finished task
        can't clash with anything.

        Returns:
            A list of human-readable warning strings, sorted by slot, or
            an empty list when nothing overlaps — so callers display a
            warning instead of hitting an exception.
        """
        by_slot: dict[tuple[date, str], list[tuple[str, Task]]] = {}
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.completed:
                    continue  # a finished task can't conflict with anything
                slot = (task.scheduled_date, task.time)
                by_slot.setdefault(slot, []).append((pet.name, task))

        warnings = []
        for (slot_date, slot_time) in sorted(by_slot):
            entries = by_slot[(slot_date, slot_time)]
            if len(entries) > 1:
                labels = ", ".join(
                    f"{name} ({task.description})" for name, task in entries
                )
                warnings.append(
                    f"⚠️ {len(entries)} tasks overlap at {slot_time} "
                    f"on {slot_date}: {labels}"
                )
        return warnings

    def has_conflicts(self) -> bool:
        """True if any two pending tasks share the same date and time."""
        return bool(self.detect_conflicts())

    def tasks_by_frequency(self, frequency: str) -> list[Task]:
        """Return tasks matching a given frequency (e.g. 'daily')."""
        return [
            task for task in self.get_all_tasks()
            if task.frequency == frequency
        ]

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return tasks filtered by completion status and/or pet name.

        Walks each pet's task list once (O(n)) and keeps a task only if it
        passes every active filter. Both filters are optional and combine
        with AND.

        Args:
            completed: ``True`` keeps only done tasks, ``False`` only
                pending; ``None`` ignores completion status.
            pet_name: keeps only that pet's tasks (case-insensitive);
                ``None`` includes every pet.

        Returns:
            A new list of the matching tasks, in each pet's insertion
            order (not time-sorted).
        """
        results = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    # --- Manage -----------------------------------------------------------

    def mark_complete(self, task: Task) -> Task | None:
        """Mark a task done and, if it recurs, queue its next occurrence.

        For a 'daily' or 'weekly' task, a fresh uncompleted instance is
        automatically added to the same pet for the next day/week and
        returned. Non-recurring tasks return None.
        """
        task.mark_done()
        follow_up = task.next_occurrence()
        if follow_up is not None:
            owning_pet = self._pet_owning(task)
            if owning_pet is not None:
                owning_pet.add_task(follow_up)
        return follow_up

    def _pet_owning(self, task: Task) -> Pet | None:
        """Return the pet whose task list contains this exact task object."""
        for pet in self.owner.pets:
            if any(t is task for t in pet.tasks):
                return pet
        return None

    def progress_summary(self) -> str:
        """Return a short summary of how many tasks are done vs. remaining."""
        all_tasks = self.get_all_tasks()
        done = len(self.completed_tasks())
        return f"{done} of {len(all_tasks)} tasks completed."
