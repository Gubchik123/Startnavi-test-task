FROM python:3.11 AS base

FROM base AS installer
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM installer as application
WORKDIR /usr/src/app
COPY . .
