from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Rifah")
    snow = Pet(name="Snow", species="cat")
    cloud = Pet(name="Cloud", species="dog")
    owner.add_pet(snow)
    owner.add_pet(cloud)

    # Add tasks deliberately OUT OF ORDER (times are not chronological)
    # so we can see sort_by_time() actually reorder them.
    snow.add_task(Task(description="Evening play", time="19:00", frequency="daily"))
    snow.add_task(Task(description="Feed breakfast", time="07:30", frequency="daily"))
    snow.add_task(Task(description="Feed dinner", time="18:00", frequency="daily"))
    cloud.add_task(Task(description="Morning walk", time="08:00", frequency="daily"))
    cloud.add_task(Task(description="Vet visit", time="14:00", frequency="weekly"))
    # Deliberate CONFLICT: Cloud's evening walk lands at 18:00, the same
    # time Snow's dinner is scheduled, so detect_conflicts() should flag it.
    cloud.add_task(Task(description="Evening walk", time="18:00", frequency="daily"))

    # Mark a couple done so the completion filter has something to show.
    snow.tasks[1].mark_done()   # Feed breakfast
    cloud.tasks[0].mark_done()  # Morning walk

    scheduler = Scheduler(owner)

    print("Insertion order (as added):")
    for task in scheduler.get_all_tasks():
        print(f"  {task.time}  {task.description}")

    print("\nSorted by time (sort_by_time):")
    for task in scheduler.sort_by_time():
        print(f"  {task.time}  {task.description}")

    print("\nSnow's tasks (filter_tasks pet_name='Snow'):")
    for task in scheduler.filter_tasks(pet_name="Snow"):
        print(f"  {task.time}  {task.description}")

    print("\nCompleted tasks (filter_tasks completed=True):")
    for task in scheduler.filter_tasks(completed=True):
        print(f"  {task.time}  {task.description}")

    print("\nPending tasks (filter_tasks completed=False):")
    for task in scheduler.filter_tasks(completed=False):
        print(f"  {task.time}  {task.description}")

    print("\nSchedule conflicts (detect_conflicts):")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts — every task has its own time slot.")

    print(f"\n{scheduler.progress_summary()}")


if __name__ == "__main__":
    main()
