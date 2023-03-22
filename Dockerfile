FROM python:3.9-slim AS build

ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

ADD src /app
WORKDIR /app

RUN pip3 install -r requirements.txt

# Minimal image
FROM gcr.io/distroless/python3:nonroot

COPY --from=build /app /app
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
CMD ["bot.py"]
