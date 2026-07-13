# apps/demo-endpoint — the read-only Columna demo endpoint

Powers **demo.datumwise.ai** (Exhibit B's live target) and doubles as the `docker run` quickstart
image. Serves ONLY the packaged demo Manifold, read-only by construction; worst-case abuse =
restart.

## Architecture

`columna-server`'s `demo --http` binds **loopback-only** when `COLUMNA_MCP_TOKEN` is unset (shipped
behaviour — the engine is never modified). So one container runs it ungated on `127.0.0.1:8765`
behind **nginx** (`0.0.0.0:8080`), the public face:

- per-IP rate limit (60 req/min, burst 20 → `429`)
- CORS scoped to `datumwise.ai`, `*.vercel.app`, `localhost`
- SSE-safe proxying (`proxy_buffering off`) for MCP streamable-http

No bearer token ever reaches the browser.

## Quickstart image

```bash
docker run --rm ghcr.io/datumwise/columna-demo demo --play   # the three-mood transcript
```

## Deploy (Fly.io)

```bash
fly deploy --config fly.toml            # app: datumwise-columna-demo
fly certs add demo.datumwise.ai         # after the CNAME is in place
```

Health check: `GET /healthz` → `ok`. The MCP endpoint is proxied at `/mcp`.
