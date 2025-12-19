from itertools import combinations
import argparse
from math import factorial
from functools import lru_cache

class SimplexLock:
    def __init__(self, buttons=5):
        self.n = buttons

    @lru_cache(None)
    def _stirling(self, n, k):
        if n == k == 0:
            return 1
        if n == 0 or k == 0:
            return 0
        return self._stirling(n - 1, k - 1) + k * self._stirling(n - 1, k)

    def count_combinations(self):
        total = 0
        n = self.n

        for k in range(1, n + 1):
            choose_subset = factorial(n) // (factorial(k) * factorial(n - k))
            for i in range(1, k + 1):
                total += factorial(i) * self._stirling(k, i) * choose_subset

        return total

    def brute_force_time(self, seconds_per_guess, worst_case=False):
        total = self.count_combinations()
        guesses = total if worst_case else total / 2
        return guesses * seconds_per_guess


def format_duration(seconds):
    seconds = int(seconds)

    units = [
        ("years", 60 * 60 * 24 * 365),
        ("days", 60 * 60 * 24),
        ("hours", 60 * 60),
        ("minutes", 60),
        ("seconds", 1),
    ]

    parts = []
    for name, unit in units:
        value = seconds // unit
        if value:
            parts.append(f"{value} {name}")
            seconds %= unit

    return ", ".join(parts) if parts else "0 seconds"


def main():
    parser = argparse.ArgumentParser(
        description="Simplex lock combinatorics and brute-force time estimation"
    )
    parser.add_argument(
        "buttons",
        type=int,
        help="Number of buttons on the lock"
    )
    parser.add_argument(
        "--seconds-per-guess",
        type=float,
        help="Time per guess in seconds"
    )
    parser.add_argument(
        "--worst-case",
        action="store_true",
        help="Assume worst-case brute-force time"
    )

    args = parser.parse_args()

    lock = SimplexLock(args.buttons)
    total = lock.count_combinations()

    print(f"Total combinations: {total}")

    if args.seconds_per_guess is not None:
        seconds = lock.brute_force_time(
            args.seconds_per_guess,
            worst_case=args.worst_case
        )
        print("Estimated brute-force time:", format_duration(seconds))


if __name__ == "__main__":
    main()

