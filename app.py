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
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    schedule = scheduler.daily_schedule()

    if schedule:
        for task in schedule:
            status = "✅" if task.completed else "⬜"
            st.write(f"{status} **{task.time}** — {task.description} ({task.frequency})")
        st.caption(scheduler.progress_summary())
    else:
        st.info("No tasks scheduled yet. Add some tasks above.")
