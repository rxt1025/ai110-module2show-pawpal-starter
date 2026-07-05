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
    My schedular detect_conflicts() flags a conflict only when two tasks share the exact same (date, time) slot. 
- Why is that tradeoff reasonable for this scenario?
     A pet owner has a handful of daily tasks (feed, walk, meds), not hundreds of tightly-packed appointments. With so few tasks, the odds that two near-adjacent tasks genuinely collide are low and even if they do, the owner can eyeball the sorted table and shuffle things themselves. 
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used AI to implement the instructions according to the project phases.
- What kinds of prompts or questions were most helpful?
   The most helpful prompts were the UI and Backend Integration prompts.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    When I added recurrence, the first version of the Task class stored the date in a field literally named date but date was also the name I'd imported from Python's datetime module. My editor's linter immediately flagged it and I realized the field name was shadowing the type. Even though the code happened to still run, I rejected that version and renamed the field to scheduled_date, which is both unambiguous and more descriptive.
- How did you evaluate or verify what the AI suggested?
    I wrote a 12-test pytest suite covering the specific behaviors and edge cases. For the UI, I launched Streamlit headless and checked it returned HTTP 200 with no errors before trusting it. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested sorting, filtering, recurrence, and conflict detection.
- Why were these tests important?
    These tests were importent because they are the actual logic a pet owner relies on. Because if they broke the daily plan would be wrong or misleading. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
    I am firmly convince that my schedular works correctly because I tested with different commands and got 12 successful passed results.
- What edge cases would you test next if you had more time?
    I would test invalid time input like 9:00 or 25:00.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I'm most satisfied with how the recurrence and conflict-detection features came together cleanly on top of the original class design without needing to rewrite it

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I'd replace the string-based time with a real datetime/time type and add a duration field. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    The biggest thing I learned is that AI suggestions are a starting point, not an answer
