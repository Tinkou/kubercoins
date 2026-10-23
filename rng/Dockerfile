FROM python:3.15-alpine

WORKDIR /app

RUN pip install --no-cache-dir Flask

COPY rng.py .

ENV PORT=80

EXPOSE 80

CMD ["python", "rng.py"]
