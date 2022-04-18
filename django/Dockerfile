# Taken from
FROM python:3.9.5 as base

ENV PYTHONUNBUFFERED 1

WORKDIR /app

FROM base as release

COPY ./requirements.txt /requirements.txt

EXPOSE 8000

# to enable Apple Silicon M1
RUN apt-get update \
    # we cannot revert libpq as this installs multiple so files.
    && apt-get -y install libpq-dev \
    && apt-get -y install gcc \
    && pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /requirements \
    && apt-get purge --auto-remove -yy $(cat /var/log/apt/history.log | tail -n2 | head -n 1 | sed -e 's,: ,\n,' -e 's/:[a-z]\|), /\n/g' | awk 'NR % 2 == 0') \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
