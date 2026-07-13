# The public demo endpoint (demo.datumwise.ai) AND the `docker run` quickstart image.
#
# columna-server's `demo --http` binds LOOPBACK-ONLY when COLUMNA_MCP_TOKEN is unset (shipped
# behaviour — we do not change the engine). So we run it ungated on 127.0.0.1 behind nginx, which
# is the public face: per-IP rate limiting, CORS, SSE-safe proxying. No token ever reaches the
# browser; only the read-only packaged demo Manifold is served; worst-case abuse = restart.
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx \
    && rm -rf /var/lib/apt/lists/*

# pinned to the versions the site's query pins were verified against
RUN pip install --no-cache-dir "columna-core==0.7.8" "columna-server==0.1.0"

COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# bare `docker run <image>` plays the three-mood demo; Fly overrides with `serve-http`.
CMD ["demo", "--play"]
