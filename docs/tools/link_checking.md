# Link checking the site — the Zenodo trap

There is no automated link checker in this repo yet. When one is written, or when a link sweep is done
by hand (launch checklist v1, steps 4 and 6 both call for one), read this first.

## Zenodo UA-filters. A 403 on a DOI is the filter, not a dead link.

Every paper in the corpus resolves through `https://doi.org/10.5281/zenodo.<id>`, and Zenodo rejects
requests whose `User-Agent` looks automated. The rejection is a blanket **HTTP 403** — indistinguishable
at a glance from a genuinely broken link, and it hits **every DOI at once**.

Observed 2026-07-25 against the six published DOIs:

| User-Agent | result |
|---|---|
| `python-urllib`, `curl/8.x`, or `Mozilla/5.0` (bare) | **403 on all six** |
| A full browser UA string | **200 on all six** |

A naive checker will therefore report the entire research corpus as dead. It is not. Before filing a
broken-link bug against a DOI, re-check with a full browser UA:

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
curl -sIL -o /dev/null -w '%{http_code}\n' -A "$UA" "https://doi.org/10.5281/zenodo.21553379"
```

Note `-L`: `doi.org` 302-redirects to `zenodo.org`, so a checker that does not follow redirects sees a
3xx and may score it a failure on that ground instead.

**Rule for any checker written later:** send a full browser UA, follow redirects, and treat a 403 from
`zenodo.org` as *inconclusive* — surface it for a human to eyeball rather than failing the build. The
failure that matters is a 404 or a DNS failure, not a bot filter.

## What actually needs checking

- The six DOIs (`/about`, the footer, `/ladder`, `/benchmark`, and the evidence footers inside the two
  `/positions` pieces).
- `github.com/datumwise/columna` and `github.com/datumwise/ground-truth-benchmark`.
- Internal routes — these are the ones a checker genuinely earns its keep on, since a renamed page
  is a silent 404 and Astro will not warn about a stale `href`.
