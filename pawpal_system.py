"""PawPal+ core system — class skeleton.

Generated from diagrams/uml.mmd. Attributes and method signatures only;
the logic is intentionally left unimplemented (stubs) for now.
"""

from dataclasses import dataclass, field


@dataclass
class CareTask:
    """A single pet-care task (e.g., Feed, Walk, Bath)."""

    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"


@dataclass
class Pet:
    """A pet owned by the user, with its list of care tasks."""

    name: str
    species: str  # "dog" | "cat" | "other"
    tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Attach a care task to this pet."""
        pass


@dataclass
class Owner:
    """The pet owner and their available time budget for the day."""

    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        pass


class Scheduler:
    """Builds and explains a daily care plan under time/priority constraints."""

    def __init__(self, tasks: list[CareTask], available_minutes: int):
        self.tasks = tasks
        self.available_minutes = available_minutes

    def build_schedule(self) -> list[CareTask]:
        """Return the ordered list of tasks that fit the time budget,
        chosen and ordered by priority."""
        pass

    def explain(self) -> str:
        """Return a human-readable explanation of why the plan looks the way it does."""
        pass
