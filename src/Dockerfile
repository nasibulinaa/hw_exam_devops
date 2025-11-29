FROM python:3.12.3-alpine3.20 AS builder

# ONLINE step, download dependencies
RUN apk add build-base
COPY requirements.txt .
RUN --mount=type=cache,id=pip-cache,target=/root/.cache/pip \
    pip wheel -r requirements.txt -w wheels/

# OFFLINE step, install dependencies and copy app files
FROM python:3.12.3-alpine3.20
RUN apk add build-base
# Do not trigger rebuild of this layers if requirements was not changed
COPY requirements.txt .
RUN --mount=type=bind,from=builder,source=wheels,target=/wheels \
    pip install --no-index --find-links /wheels -r requirements.txt  
COPY . .

ENV FLASK_ENV=production

CMD ["python", "app.py"]

RUN apk add wget
# https://stackoverflow.com/questions/47722898/how-can-i-make-a-docker-healthcheck-with-wget-instead-of-curl
HEALTHCHECK  --interval=5s --timeout=3s --start-period=5s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5000/healthcheck || exit 1
