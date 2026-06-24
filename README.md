# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

The purpose of the game is to guess the randomly generated number correctly and it gives hints as too if we are higher or lower than the number. Some bugs found were that the hints were inaccurate sometimes and it didnt reset properly when user clicks new game. To fix these, I refactored the core logic out of app.py into logic_utils.py, verified and locked in the correct high/low hint direction in check_guess with pytest tests, and corrected the New Game reset so the secret, score, attempts, and history all clear fully.
## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start new game → range 1–100, 8 attempts
2. Guess 40 → "Too Low" → Go HIGHER!
3. Guess 90 → "Too High" → Go LOWER! (the verified high/low direction)
4. Score, attempts-left, and history update each guess
5. Guess 70 → "Correct!" + balloons, reveals secret/score, ends until New Game resets state

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

### Challenge 4: Enhanced Game UI

I added structured, friendlier output without touching the core game logic (all 7 pytest cases still pass). Three enhancements:

- **🔥 Hot/Cold proximity hints (emoji).** New function `get_proximity(guess, secret, low, high)` in `logic_utils.py` returns a cosmetic `(label, emoji)` describing *how close* a guess is, scaled to the active range so "hot" means the same on Easy (1–20) and Normal (1–100): `🎯 Bullseye → 🔥 Burning hot → 🌶️ Hot → ♨️ Warm → ❄️ Cool → 🧊 Freezing`. It is kept deliberately **separate** from `check_guess`, so it can never change the win/lose outcome or the locked-in high/low direction.

- **🎨 Color-coded + emoji hints.** In `app.py`, the per-guess hint now appends the proximity read-out to the existing direction message and renders it through Streamlit's color-coded callouts — e.g. `st.warning("👆 Go HIGHER!  ·  🔥 Burning hot")`, `st.success(...)` on a win, `st.error(...)` on loss/invalid input.

- **📊 Session summary table + scoreboard.** New `render_session_summary()` function in `app.py` displays a 3-metric scoreboard (`st.metric`: Score, Guesses made, Attempts left) and a per-guess recap table (`st.table`) with columns `# / Guess / Result / Proximity`. To support this, history entries changed from bare values to labeled dicts (invalid input shows a `⚠️ Invalid` row). The summary renders both during play and on the frozen win/lose screen so players can review the whole run.

**Functions modified/added:**
- `logic_utils.py` → **added** `get_proximity(...)`
- `app.py` → **added** `render_session_summary()`; **modified** the guess-processing block (structured history + proximity-enriched hint) and the end-screen rendering.

**Screenshot** *(optional)*: <!-- Insert a screenshot of the enhanced UI here -->

