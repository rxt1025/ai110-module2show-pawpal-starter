"""Tests for the PawPal+ scheduling logic.

Run with:  pytest        (or)  .venv/bin/pytest -v
"""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def make_owner() -> Owner:
    """Build a small owner/pet/task fixture used by several tests."""
    owner = Owner(name="Rifah")
    snow = Pet(name="Snow", species="cat")
    cloud = Pet(name="Cloud", species="dog")
    owner.add_pet(snow)
    owner.add_pet(cloud)

    # Added out of chronological order on purpose.
    snow.add_task(Task(description="Evening play", time="19:00", frequency="daily"))
    snow.add_task(Task(description="Feed breakfast", time="07:30", frequency="daily"))
    cloud.add_task(Task(description="Morning walk", time="08:00", frequency="daily"))
    return owner


# --- sorting ------------------------------------------------------------------

def test_sort_by_time_orders_chronologically():
    scheduler = Scheduler(make_owner())
    times = [task.time for task in scheduler.sort_by_time()]
    assert times == ["07:30", "08:00", "19:00"]


def test_sort_by_time_does_not_mutate_original():
    owner = make_owner()
    scheduler = Scheduler(owner)
    before = [t.time for t in owner.pets[0].tasks]
    scheduler.sort_by_time()
    after = [t.time for t in owner.pets[0].tasks]
    assert before == after  # sorted() returns a new list


# --- filtering ----------------------------------------------------------------

def test_filter_tasks_by_pet_name_is_case_insensitive():
    scheduler = Scheduler(make_owner())
    snow_tasks = scheduler.filter_tasks(pet_name="snow")
    assert {t.description for t in snow_tasks} == {"Evening play", "Feed breakfast"}


def test_filter_tasks_by_completion_status():
    owner = make_owner()
    owner.pets[0].tasks[0].mark_done()
    scheduler = Scheduler(owner)
    assert len(scheduler.filter_tasks(completed=True)) == 1
    assert len(scheduler.filter_tasks(completed=False)) == 2


def test_filter_tasks_no_filters_returns_everything():
    scheduler = Scheduler(make_owner())
    assert len(scheduler.filter_tasks()) == 3


# --- recurrence ---------------------------------------------------------------

def test_daily_task_next_occurrence_is_one_day_later():
    task = Task(description="Feed", time="07:30", frequency="daily",
                scheduled_date=date(2026, 7, 5))
    follow_up = task.next_occurrence()
    assert follow_up.scheduled_date == date(2026, 7, 6)
    assert follow_up.completed is False


def test_weekly_task_next_occurrence_is_one_week_later():
    task = Task(description="Vet", time="14:00", frequency="weekly",
                scheduled_date=date(2026, 7, 5))
    assert task.next_occurrence().scheduled_date == date(2026, 7, 12)


def test_one_off_task_has_no_next_occurrence():
    task = Task(description="Nail trim", time="10:00", frequency="once")
    assert task.next_occurrence() is None


def test_mark_complete_auto_creates_next_recurring_instance():
    owner = make_owner()
    snow = owner.pets[0]
    scheduler = Scheduler(owner)
    before = len(snow.tasks)

    daily = snow.tasks[0]  # "Evening play", daily
    follow_up = scheduler.mark_complete(daily)

    assert daily.completed is True
    assert follow_up is not None
    assert len(snow.tasks) == before + 1  # a fresh instance was queued
    assert follow_up.scheduled_date == daily.scheduled_date + timedelta(days=1)


# --- conflict detection -------------------------------------------------------

def test_detect_conflicts_flags_cross_pet_overlap():
    owner = make_owner()
    # Cloud's evening walk collides with Snow's evening play at 19:00.
    owner.pets[1].add_task(Task(description="Evening walk", time="19:00",
                                frequency="daily"))
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert scheduler.has_conflicts() is True
    assert len(conflicts) == 1
    assert "19:00" in conflicts[0]


def test_no_conflicts_when_all_times_differ():
    scheduler = Scheduler(make_owner())
    assert scheduler.detect_conflicts() == []
    assert scheduler.has_conflicts() is False


def test_completed_task_does_not_count_as_conflict():
    owner = make_owner()
    owner.pets[1].add_task(Task(description="Evening walk", time="19:00",
                                frequency="daily"))
    owner.pets[0].tasks[0].mark_done()  # complete Snow's 19:00 task
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []  # only one pending 19:00 task left
