# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```
====================================== test session starts =======================================
platform darwin -- Python 3.11.5, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/_rifahtasfia/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 12 items                                                                               

test_pawpal_system.py ............                                                         [100%]

======================================= 12 passed in 0.01s =======================================

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

## Testing PawPal+
command: .venv/bin/pytest -v
====================================== test session starts =======================================
platform darwin -- Python 3.11.5, pytest-9.1.1, pluggy-1.6.0 -- /Users/_rifahtasfia/ai110-module2show-pawpal-starter/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/_rifahtasfia/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 12 items                                                                               

test_pawpal_system.py::test_sort_by_time_orders_chronologically PASSED                     [  8%]
test_pawpal_system.py::test_sort_by_time_does_not_mutate_original PASSED                   [ 16%]
test_pawpal_system.py::test_filter_tasks_by_pet_name_is_case_insensitive PASSED            [ 25%]
test_pawpal_system.py::test_filter_tasks_by_completion_status PASSED                       [ 33%]
test_pawpal_system.py::test_filter_tasks_no_filters_returns_everything PASSED              [ 41%]
test_pawpal_system.py::test_daily_task_next_occurrence_is_one_day_later PASSED             [ 50%]
test_pawpal_system.py::test_weekly_task_next_occurrence_is_one_week_later PASSED           [ 58%]
test_pawpal_system.py::test_one_off_task_has_no_next_occurrence PASSED                     [ 66%]
test_pawpal_system.py::test_mark_complete_auto_creates_next_recurring_instance PASSED      [ 75%]
test_pawpal_system.py::test_detect_conflicts_flags_cross_pet_overlap PASSED                [ 83%]
test_pawpal_system.py::test_no_conflicts_when_all_times_differ PASSED                      [ 91%]
test_pawpal_system.py::test_completed_task_does_not_count_as_conflict PASSED               [100%]

======================================= 12 passed in 0.01s =======================================

Brief Description: All 12 passed meaning the algorithmic features sorting, filtering, auto-recurrence, and conflict detection — all behave correctly, including their edge cases (case-insensitivity, non-mutation, one-off tasks, completed-task handling).