"""Drop the technical answer cache. Run after any change that moves the corpus underneath it.

WHEN. A work is superseded, a source is re-ruled, the index is rebuilt, or a deposit is refreshed.
In each case the cache holds answers whose citations describe a world that no longer exists, and it
will keep serving them for up to the full TTL. Expiry cannot help: expiry measures elapsed time, and
nothing about a supersession is about time.

WHAT IT DOES NOT DO. It does not touch the answers. A cached answer and a stored answer are
different objects (see the schema comment in store.py) and the stored one is evidence — of what Ask
said on a day when the corpus said something else. Deleting that would erase the only record of the
drift.
"""

from __future__ import annotations

from . import store


def main() -> None:
    n = store.cache_purge()          # expired entries, always worth clearing
    m = store.cache_drop_all()
    print(f"answer cache cleared: {m + n} entr{'y' if m + n == 1 else 'ies'} dropped "
          f"({n} already expired). Stored answers untouched.")


if __name__ == "__main__":
    main()
