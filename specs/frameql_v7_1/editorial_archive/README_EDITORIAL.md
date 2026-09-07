# Editorial archive

This archive contains output/ (the active review set), sources/ (preserved historical local files and normalized full web-text transcriptions), audit/ (source hashes, exact recorded edits, diffs and document checks), and the scripts used to create and inspect the new documents.

Start with output/START_HERE.md. Historical sources are NOT active guidance. The authority index lists their supersession dispositions. Introduction and Primer diffs are against normalized full-text transcriptions, not original deposit bytes. No mathematical or Columna suite was executed. The 40 semantic cases are review requirements.

To rerun document checks in an environment with Python and markdown-it-py, run `python audit_documents.py` from the archive root. Rendering additionally requires Pandoc, PyYAML and BeautifulSoup; browser preview requires Playwright and an available Chromium executable. This is document tooling, not Columna implementation code.
