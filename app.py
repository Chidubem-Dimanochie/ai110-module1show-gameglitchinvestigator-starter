import random
import streamlit as st

# FIX: Refactored the game logic into logic_utils.py using agent mode and
# replaced the inline function definitions with this import.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    # CHALLENGE 4 (Enhanced UI): cosmetic Hot/Cold proximity helper.
    get_proximity,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


# CHALLENGE 4 (Enhanced UI): a single, reusable renderer for the live
# scoreboard + a per-guess summary table. It only reads session state, so it's
# safe to call both mid-game and on the frozen win/lose screen.
def render_session_summary():
    st.divider()
    st.subheader("📊 Session Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Score", st.session_state.score)
    col2.metric("Guesses made", len(st.session_state.history))
    col3.metric(
        "Attempts left",
        max(0, attempt_limit - st.session_state.attempts),
    )

    if st.session_state.history:
        # st.session_state.history holds one dict per guess (see below), so
        # Streamlit renders it as a clean, color-free table of the whole run.
        st.table(st.session_state.history)
    else:
        st.caption("No guesses yet — make your first guess above! 👆")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIX (diagnosed with the AI agent, applied in agent mode): the Developer Debug
# Info panel above was moved up here, above "Make a guess" where it belongs.
# It previously rendered at the bottom of the page.
st.subheader("Make a guess")

# FIX: I reported that "New Game" appeared dead after a win/loss; the AI agent
# traced it to the reset leaving status/score/history untouched and rewrote it
# to fully reset state. Diagnosed together, applied in agent mode.
# New Game lives ABOVE the form so the reset can clear the guess input too.
# A widget's value can't be modified after the widget is created in the same
# run, so clearing the text box has to happen before the form is built below.
new_game = st.button("New Game 🔁")
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state[f"guess_input_{difficulty}"] = ""
    st.rerun()

# FIX: I described the "have to click Submit twice" symptom; the AI agent
# identified it as Streamlit committing the text box and the button press in
# separate reruns, and suggested wrapping them in a form. Pair-fixed in agent mode.
# Wrapping the input and submit button in a form makes typing + clicking
# register in a SINGLE rerun. Without it, the first click only commits the
# text box and you'd have to click "Submit" twice.
with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}",
    )
    submit = st.form_submit_button("Submit Guess 🚀")

show_hint = st.checkbox("Show hint", value=True)

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    # CHALLENGE 4 (Enhanced UI): still show the full recap on the frozen
    # end screen so players can review every guess they made.
    render_session_summary()
    st.stop()

# FIX: I noticed the history/attempts lagged one click behind; the AI agent
# explained Streamlit's top-to-bottom rerun model and we reordered processing
# to run before the display panels. Collaboratively reworked in agent mode.
# Process the guess BEFORE rendering the panels below, so attempts-left and
# history reflect THIS click instead of lagging one click behind.
result = None
if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        # CHALLENGE 4 (Enhanced UI): history rows are dicts so the Session
        # Summary table has labeled columns. Invalid input still gets a row.
        st.session_state.history.append(
            {
                "#": st.session_state.attempts,
                "Guess": raw_guess,
                "Result": "⚠️ Invalid",
                "Proximity": "—",
            }
        )
        result = ("error", err)
    else:
        # FIX: AI caught that the secret was being cast to str() on even
        # attempts, breaking the comparison; we now always pass the raw int.
        # Found via agent-mode review, I verified and kept it.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        # CHALLENGE 4 (Enhanced UI): cosmetic Hot/Cold read-out. Kept fully
        # separate from check_guess/update_score so it can't alter game logic.
        prox_label, prox_emoji = get_proximity(
            guess_int, st.session_state.secret, low, high
        )

        st.session_state.history.append(
            {
                "#": st.session_state.attempts,
                "Guess": guess_int,
                "Result": outcome,
                "Proximity": f"{prox_emoji} {prox_label}",
            }
        )

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            result = (
                "success",
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}",
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            result = (
                "error",
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}",
            )
        else:
            # CHALLENGE 4 (Enhanced UI): bolt the Hot/Cold emoji onto the
            # color-coded direction hint, e.g. "👆 Go HIGHER!  ·  🔥 Burning hot".
            result = ("hint", f"{message}  ·  {prox_emoji} {prox_label}")

# Render up-to-date state now that the guess has been processed.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

if result is not None:
    kind, text = result
    if kind == "success":
        st.success(text)
    elif kind == "error":
        st.error(text)
    elif kind == "hint" and show_hint:
        st.warning(text)

# CHALLENGE 4 (Enhanced UI): live scoreboard + per-guess recap table.
render_session_summary()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
