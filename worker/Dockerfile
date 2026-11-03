FROM python:alpine
RUN pip install redis
RUN pip install requests debugpy
COPY healthcheck.sh /usr/local/bin/
RUN chmod a+x /usr/local/bin/healthcheck.sh
COPY worker.py healthcheck.sh /
CMD ["python", "worker.py"]
