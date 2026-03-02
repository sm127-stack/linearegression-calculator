FROM python:3.11-slim

WORKDIR /app

# Install nginx + envsubst (gettext-base)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx gettext-base \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=10000

# Nginx needs a config; we generate it from the template using envsubst at runtime.
CMD sh -c "\
  gunicorn -b 127.0.0.1:8000 server:app & \
    voila /app --no-browser \
          --Voila.ip=127.0.0.1 \
          --Voila.port=8866 \
          --Voila.base_url=/voila/ &
  envsubst '\$PORT' < /app/nginx.conf.template > /etc/nginx/nginx.conf && \
  nginx -g 'daemon off;' \
"
