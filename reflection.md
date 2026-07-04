# PawPal+ Project Reflection

## 1. System Design

3 core actions a user should be able to perform:
    1.add a pet
    2.schedule a walk
    3.see today's tasks

**a. Initial design**

- Briefly describe your initial UML design.
    My initial UML design is called "PawPal+" and has four classes.The classes include owner name, pet name, species, Tasks, and build schedule.

- What classes did you include, and what responsibilities did you assign to each?
    I include four classes including owner name, pet name, species, Tasks, and build schedule.
    I assign my name "Rifah" under owner name. I added "Snow" under pet name. For the species I choose cat. I added three tasks feed, walk, and bath.And finally the build schedule isn't implemented yet.

**b. Design changes**

- Did your design change during implementation?
    Yes.
- If yes, describe at least one change and why you made it.
    Added Owner.all_tasks() which collects tasks across all pets. It gives owner a way to collect all its tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    My scheduler consider task title, time and priority. The task title has feed, walk, and bath. The duration contains 24, 30, and, 10 minutes. 
- How did you decide which constraints mattered most?
    feeding matters the most because I label this under high priority.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
