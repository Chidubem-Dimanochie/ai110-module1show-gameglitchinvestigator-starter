# FIX: Extracted the four core game-logic functions out of app.py into this
# module. I described the glitchy game to the AI agent and asked it to refactor
# the logic away from the Streamlit UI; the agent moved these functions here.


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"

    If the guess is greater than the secret, the player guessed TOO HIGH and
    should aim lower; if it's smaller, they guessed TOO LOW and should aim
    higher.
    """
    # FIX: This was flagged as the suspected high/low bug. The AI agent and I
    # reviewed it together and confirmed the direction is actually correct
    # (guess > secret -> "Too High" -> go LOWER). Locked it in with regression
    # tests in test/test_game_logic.py instead of "fixing" working code.
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "👇 Go LOWER!"
    else:
        return "Too Low", "👆 Go HIGHER!"


# CHALLENGE 4 (Enhanced UI): cosmetic "Hot/Cold" proximity feedback.
# This is intentionally kept separate from check_guess so it can NEVER change
# the win/lose outcome or the high/low direction the regression tests lock in
# -- it only describes HOW CLOSE the guess is, not which way to go.
def get_proximity(guess: int, secret: int, low: int, high: int):
    """
    Return (label, emoji) describing how close `guess` is to `secret`,
    scaled to the size of the active range so "hot" means the same thing
    on Easy (1-20) and Normal (1-100).

    Purely cosmetic: does not affect scoring or the Too High / Too Low result.
    """
    span = max(1, high - low)
    ratio = abs(guess - secret) / span

    if ratio == 0:
        return "Bullseye", "🎯"
    if ratio <= 0.05:
        return "Burning hot", "🔥"
    if ratio <= 0.15:
        return "Hot", "🌶️"
    if ratio <= 0.30:
        return "Warm", "♨️"
    if ratio <= 0.50:
        return "Cool", "❄️"
    return "Freezing", "🧊"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
