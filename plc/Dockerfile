FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pymodbus==3.6.9
COPY shared/ /app/shared/
COPY plc/plc_server.py /app/
ENV PYTHONPATH=/app
CMD ["python3", "-u", "plc_server.py"]
