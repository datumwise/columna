"""Acceptance check for `columna-server demo --play`, read from stdin.

Extracted from an inline `python -c` in ci.yml when the demo-wheel-install job gained a Windows
leg (0.13.2). The inline form depended on POSIX shell quoting; a file does not, so the same
assertion runs byte-identically on ubuntu-latest and windows-latest. One check, two platforms —
if the two legs could drift, the Windows leg would prove less than it appears to.

Asserts: all four moods present, in contract order, on contract version 3.
"""

import sys

MOODS = ("clarify", "refuse", "disclose", "serve")


def main() -> int:
    payload = sys.stdin.read()

    positions = [payload.find('"outcome": "%s"' % mood) for mood in MOODS]

    missing = [mood for mood, pos in zip(MOODS, positions) if pos == -1]
    if missing:
        print("FAIL: mood(s) never appeared in demo --play output: %s" % ", ".join(missing))
        print("---- output was %d bytes ----" % len(payload))
        print(payload[:2000])
        return 1

    if positions != sorted(positions):
        ordering = ", ".join("%s@%d" % pair for pair in zip(MOODS, positions))
        print("FAIL: moods appeared out of contract order: %s" % ordering)
        return 1

    if '"contract_version": "3"' not in payload:
        print('FAIL: no \'"contract_version": "3"\' in demo --play output')
        return 1

    # ASCII ONLY, deliberately. This file is the harness that proves the product handles non-ASCII
    # on a legacy codepage; it must not itself depend on one. The first Windows run printed its
    # em-dash only because cp1252 happens to have one at 0x97 — U+2500, four lines earlier in the
    # product's own output, does not, which is exactly where the crash landed. A guard that can be
    # broken by the condition it guards against is not a guard.
    print("demo --play OK - four moods in contract order, contract_version 3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
