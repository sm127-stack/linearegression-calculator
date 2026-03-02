#!/usr/bin/env sh
set -e

# Start Flask (internal)
gunicorn -b 127.0.0.1:8000 server:app &

# Start Voilà (internal) and point it at /app so it can see the notebooks
voila /app --no-browser \
  --Voila.ip=127.0.0.1 \
  --Voila.port=8866 \
  --Voila.base_url=/voila/ \
  --show_tracebacks=True &

# Generate nginx.conf from template using Render's PORT
envsubst '$PORT' < /app/nginx.conf.template > /etc/nginx/nginx.conf

# Run nginx in foreground (public)
nginx -g "daemon off;"
