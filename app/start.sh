#!/usr/bin/env sh
set -e

# Flask
gunicorn -b 127.0.0.1:8000 server:app &

# Voilà (show tracebacks so notebook errors are visible)
voila /app --no-browser \
  --Voila.ip=127.0.0.1 \
  --Voila.port=8866 \
  --Voila.base_url=/voila/ \
  --show_tracebacks=True &

# Nginx config
envsubst '$PORT' < /app/nginx.conf.template > /etc/nginx/nginx.conf

# Nginx in foreground
nginx -g "daemon off;"
