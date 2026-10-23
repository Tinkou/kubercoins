FROM python:alpine
RUN pip install redis
RUN pip install requests debugpy
COPY worker.py /
CMD ["python", "worker.py"]
