import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant — add pets, add tasks, see today's schedule.")

# --- Persistent state ---------------------------------------------------------
# Create the Owner once and keep it in the session "vault" so pets and tasks
# survive across reruns instead of being rebuilt on every click.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

# --- Add a Pet ----------------------------------------------------------------
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species))
    st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    st.write("Your pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species}) — {len(pet.tasks)} task(s)")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a Task ---------------------------------------------------------------
st.subheader("Add a Task")
if owner.pets:
    pet_choice = st.selectbox("Which pet?", [pet.name for pet in owner.pets])
    col1, col2, col3 = st.columns(3)
    with col1:
        description = st.text_input("Task description", value="Morning walk")
    with col2:
        time = st.text_input("Time (HH:MM)", value="08:00")
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly"])

    if st.button("Add task"):
        # Find the selected Pet object and attach the new Task to it.
        pet = next(p for p in owner.pets if p.name == pet_choice)
        pet.add_task(Task(description=description, time=time, frequency=frequency))
        st.success(f"Added '{description}' to {pet.name}.")
else:
    st.info("Add a pet first, then you can give it tasks.")

st.divider()

# --- Today's Schedule ---------------------------------------------------------
st.subheader("Today's Schedule")
if not owner.pets or not owner.all_tasks():
    st.info("No tasks scheduled yet. Add some tasks above.")
else:
    scheduler = Scheduler(owner)

    # Conflict warnings — st.warning shows any two tasks sharing a time slot.
    conflicts = scheduler.detect_conflicts()
    for warning in conflicts:
        st.warning(warning)

    # Filter controls wired to Scheduler.filter_tasks().
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        pet_filter = st.selectbox(
            "Filter by pet", ["All pets"] + [pet.name for pet in owner.pets]
        )
    with fcol2:
        status_filter = st.radio(
            "Show", ["All", "Pending", "Completed"], horizontal=True
        )

    completed = {"Pending": False, "Completed": True}.get(status_filter)
    pet_name = None if pet_filter == "All pets" else pet_filter

    # Filter, then sort the result chronologically by time.
    tasks = sorted(
        scheduler.filter_tasks(completed=completed, pet_name=pet_name),
        key=lambda task: task.time,
    )

    if tasks:
        # Map each task back to its pet (by identity) for the Pet column.
        pet_of = {id(t): pet.name for pet in owner.pets for t in pet.tasks}
        st.table([
            {
                "Time": task.time,
                "Pet": pet_of.get(id(task), "?"),
                "Task": task.description,
                "Frequency": task.frequency,
                "Status": "✅ Done" if task.completed else "⬜ Pending",
            }
            for task in tasks
        ])
        st.caption(scheduler.progress_summary())
    else:
        st.info("No tasks match the current filter.")

    # Mark a task done — triggers auto-recurrence for daily/weekly tasks.
    pending = scheduler.filter_tasks(completed=False)
    if pending:
        labels = [f"{t.time} — {t.description}" for t in pending]
        choice = st.selectbox("Mark a task done", labels)
        if st.button("Mark done"):
            task = pending[labels.index(choice)]
            follow_up = scheduler.mark_complete(task)
            st.success(f"Completed '{task.description}'.")
            if follow_up is not None:
                st.info(
                    f"Next {task.frequency} occurrence scheduled for "
                    f"{follow_up.scheduled_date}."
                )
            st.rerun()
