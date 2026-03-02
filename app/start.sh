#!/usr/bin/env sh
set -e

# Start Flask (internal)
gunicorn -b 127.0.0.1:8000 server:app &

# Start Voilà (internal)
voila /app --no-browser \
  --Voila.ip=127.0.0.1 \
  --Voila.port=8866 \
  --Voila.base_url=/voila/ \
  --show_tracebacks=True &

# Nginx config
envsubst '$PORT' < /app/nginx.conf.template > /etc/nginx/nginx.conf

# Run nginx in foreground (public)
nginx -g "daemon off;"
