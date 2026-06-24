import os
import sys

import pytest

# Make logic_utils.py (in the project root) importable regardless of how
# pytest is invoked.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic_utils import check_guess


# ---------------------------------------------------------------------------
# Regression tests for the high/low direction bug in check_guess.
#
# The classic glitch is an inverted comparison: telling the player to go
# LOWER when their guess was already too low (or vice versa). These tests
# lock in the correct direction so the bug can never silently come back.
# ---------------------------------------------------------------------------


def test_guess_higher_than_secret_is_too_high():
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    # When you're too high, you must be told to go LOWER.
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()


def test_guess_lower_than_secret_is_too_low():
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    # When you're too low, you must be told to go HIGHER.
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()


def test_exact_guess_is_a_win():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


@pytest.mark.parametrize(
    "guess, secret, expected",
    [
        (51, 50, "Too High"),  # just one above the secret
        (49, 50, "Too Low"),   # just one below the secret
        (100, 1, "Too High"),  # far above
        (1, 100, "Too Low"),   # far below
    ],
)
def test_high_low_direction_at_boundaries(guess, secret, expected):
    outcome, _ = check_guess(guess, secret)
    assert outcome == expected
