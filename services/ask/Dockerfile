# Ask datumwise — the whole service.
#
# No requirements.txt and no pip install: the service is stdlib-only Python. That is not minimalism
# for its own sake — this repo runs a dependency cap guard, and every dependency added to a public,
# model-calling, internet-facing surface is attack surface on the one property whose product claim is
# "we do not misstate our own record".
#
# The image carries the registries because standing is DERIVED at request time, never typed: the
# identifier gate reads records.json to decide whether a DOI in a generated answer is real. Copying
# the registry in is what makes that check possible without a network call.
#
# Build context is the REPO ROOT, so the paths below resolve the way ask/verify.py expects
# (REPO = parents[3] of ask/verify.py, i.e. /app).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ASK_DB=/data/ask.db \
    PORT=8080

WORKDIR /app

# Registries first — they change less often than the service code, so the layer caches well.
COPY registry/publications/records.json  registry/publications/records.json
COPY registry/publications/works.json    registry/publications/works.json
COPY registry/sources/sources.json       registry/sources/sources.json

# The retrieval index, built from the SHIPPED SITE BUILD by services/ask/ask/index_build.py and
# committed so the image needs neither node nor the website source. Regenerate with:
#   (cd apps/website && npm run build) && (cd services/ask && python3 -m ask.index_build)
COPY services/ask/index/chunks.json      services/ask/index/chunks.json

COPY services/ask/ask                    services/ask/ask

RUN useradd --uid 10001 --create-home ask && mkdir -p /data && chown -R ask:ask /data /app
USER ask

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python3 -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8080/health',timeout=4).status==200 else 1)"

WORKDIR /app/services/ask
CMD ["python3", "-m", "ask.app"]
