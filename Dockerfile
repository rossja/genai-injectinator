FROM python:3.12-slim-bookworm
WORKDIR /app
LABEL maintainer="Jason Ross <algorythm@gmail.com>"
LABEL description="tooling to help create prompt injection tests for generative ai models and apps that consume their content"

COPY src/requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .
CMD ["python", "app.py"]