FROM ubuntu:22.04

RUN cd /usr/src
RUN apt-get update && apt-get install -y curl && apt-get install build-essential -y
RUN curl https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tgz --output Python-3.11.4.tgz
RUN tar xzf Python-3.11.4.tgz 
RUN cd Python-3.11.4 && \
    ./configure --enable-optimizations
RUN make altinstall

#ENV MODEL_PATH /app/model/ggml-model-gpt4all-falcon-q4_0.bin
#
## Install curl and download model

#RUN curl https://huggingface.co/nomic-ai/gpt4all-falcon-ggml/resolve/main/ggml-model-gpt4all-falcon-q4_0.bin \
#    --output run_clm.py
#
#WORKDIR /app
#COPY requirements.txt requirements.txt
#RUN pip3 install --upgrade pip && \
#    pip3 install -r requirements.txt
#
## Copy src from parent dir to where Dockerfile is
#COPY . .