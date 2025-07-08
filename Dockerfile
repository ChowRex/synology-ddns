FROM python:3.9-slim

ARG PIP_ARGS=""
COPY . /app
WORKDIR /app

EXPOSE 8000

RUN pip install $PIP_ARGS gunicorn && \
    pip install $PIP_ARGS --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:application"]
