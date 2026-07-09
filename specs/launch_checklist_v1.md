# Launch checklist — Columna v1 (public release)

The gate from a code-complete Phase 2 (`phase-2`) to a public PyPI release of **columna-core** and
**columna-server**. Ordered; each step has a clear owner and a green/red gate. The final public flip
is a human action — the agent prepares and proves, then STOPS.

## 1. Repository home — DONE
Transfer `reeeneeee/columna` → `datumwise/columna` (GitHub preserves redirects: clones, PRs, tags,
release assets all follow). `datumwise/columna` is the canonical home.

## 2. Trusted Publishers on PyPI — DONE
Register pending Trusted Publishers for **columna-core** and **columna-server**:
owner `datumwise`, repo `columna`, workflow `publish.yml`, environment `pypi`. (OIDC — no API
tokens stored.)

## 3. Publish workflow (`.github/workflows/publish.yml`)
- **Release-tag trigger** (`on: release: [published]`, or a `v*` tag push).
- Build both sdists+wheels, then publish via **`pypa/gh-action-pypi-publish`** using **OIDC** — no
  username/password, no API token. The publish job runs in the **`pypi`** environment (must match
  the Trusted Publisher registration exactly) with **`permissions: id-token: write`** on the
  publish job only.
- **Dry-run build job on PRs** (build + `twine check`, no publish) so packaging breaks surface in
  review, not at release.

## 4. README final pass
- Quickstart install becomes `pip install columna-core columna-server` (PyPI, not editable).
- The `git clone` path moves into **Contributing** (source install for contributors only).
- Delete the pre-PyPI "install core first" caveat (moot once published).
- Every link checked against the `datumwise/columna` layout.

## 5. Verbatim transcript capture
- Re-run the REPL nonexistent-measure case against the live model; commit the **verbatim** output to
  `demos/` (it replaces any reconstructed quote in the launch post).
- Fold in the nonexistent-measure tests (live-smoke ASK assertion + hermetic backstop) if not
  already merged. *(Merged in `3d5beb0`.)*

## 6. Hygiene sweep
- `LICENSE` + `NOTICE` present and correct (Apache-2.0, Datumwise).
- **Full-history secrets scan** — no keys/tokens ever committed (the live API key was only ever in
  the gitignored `.venv/`, never tracked; verify).
- No personal/absolute paths in shipped code or docs.
- `specs/` synced to what was built; both `CHANGELOG.md` current.

## 7. Release
- Tag and cut the GitHub Release; the publish workflow fires and uploads to PyPI.
- **Final proof:** a clean venv → `pip install columna-core columna-server` **from PyPI** →
  `columna-server demo --play` prints the three moods.

## 8. Go/no-go + STOP
Report the go/no-go table (every gate item, green/red). **The public flip is not the agent's to
execute** — the human cuts the release and announces.
