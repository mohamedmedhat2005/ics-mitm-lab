FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pymodbus==3.6.9
COPY shared/ /app/shared/
COPY hmi/hmi_client.py /app/
ENV PYTHONPATH=/app
CMD ["python3", "-u", "hmi_client.py"]
