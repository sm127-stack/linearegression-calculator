FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=10000

CMD sh -c "\
  voila --no-browser --Voila.ip=0.0.0.0 --Voila.port=8866 --Voila.base_url=/voila/ & \
  gunicorn -b 0.0.0.0:${PORT} server:app \
"
