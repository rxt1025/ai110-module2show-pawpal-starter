from pawpal_system import Owner, Pet, Task, Scheduler

def main() -> None:
    owner = Owner(name="Rifah")
    snow = Pet(name="Snow", species="cat")
    cloud = Pet(name="Cloud", species="dog")
    owner.add_pet(snow)
    owner.add_pet(cloud)

    snow.add_task(Task(description="Morning walk", time="08:00", frequency="daily"))
    snow.add_task(Task(description="Feed breakfast", time="07:30", frequency="daily"))
    cloud.add_task(Task(description="Evening walk", time="18:00", frequency="daily"))
    
    scheduler = Scheduler(owner)

    print("Today's Schedule:")
    for task in scheduler.daily_schedule():
        print(task.time, task.description)


if __name__ == "__main__":
 main()