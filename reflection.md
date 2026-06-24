# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Higher than correct guess | "Go lower" hint displayed | "Go higher" hint displayed | |
| Lower than correct guess | "Go higher" hint displayed | "Go lower" hint displayed | |
| Start new game | History log fully resets | History log only partially clears | |

## Bug Reproduction Logs

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|------------|-------------------|-----------------|------------------------|
| 45 | "Go Lower" hint shown | "Go Higher" hint shown | None |
| 20 | "Go Higher" hint shown | "Go Lower" hint shown | None |
| Start New Game (button click) | Full history log resets to empty | Previous round entries remain in log; only thing to change is the expected guess | None |
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - Claude code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - AI suggested that it was compare an interger value to a string value leading to the error 
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - It changed the core visual of the application in an attempt to fix a bug with the storing of input history

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I tested the edge cases i.e higher values, empty values and lower values
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - In `test/test_game_logic.py` I ran a pytest case `(51, 50, "Too High")` — a guess one above the secret. It passed, showing the high/low direction is correct right at the boundary, where an inverted comparison would have slipped through.
- Did AI help you design or understand any tests? How?
  - Yes. Claude turned my manual edge-case checks into pytest cases and explained why boundary values catch off-by-one bugs that mid-range inputs miss.


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
