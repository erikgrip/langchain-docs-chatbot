FROM python:3.10.6-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl

COPY docker/requirements.txt requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:."

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

COPY src src
ENTRYPOINT [\
    "streamlit", \
    "run", \
    "src/app/app.py", \
    "--server.port=8501", \ 
    "--server.address=0.0.0.0", \
    "--"]
