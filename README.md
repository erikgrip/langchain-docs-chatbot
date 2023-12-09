# langchain-docs-chatbot

Create a chatbot app to answer questions about langchain based on the langchain documentation.

## Table of contents

- [General info](#general-info)
- [Technologies](#technologies)
- [Running the app](#running-the-app)
- [Development Setup](#development-setup)

## General info

This is a project to build a chatbot app, that can answer questions about the python package langchain. The app was built using OpenAI's GPT4 in the autumn of 2023. Even though the model itself was not aware of langchain at the time, due to its lknowledge cutoff, the app can search information about langchain from a vector store that is loaded with the markdown filea from langchain's Github repository.

> **User:**
>
> > What is the purpose of langchain?
>
> **Assistant:**
>
> > It appears that there might be some confusion about the term "langchain". As of now, there is not enough information available specific to a tool, technology, or platform named "Langchain". The term may have been misspelled or misunderstood. If it's related to programming, blockchain, or any other specific field, please provide additional context for a more accurate answer.
>
> -- _GPT4, 7 December 2023_

What interaction with the app looks like:

https://github.com/erikgrip/langchain_docs_chatbot/assets/72067855/4afc714e-9287-47e5-84f3-16e2f05766da


## Technologies

The project was created using

- Python
- Vector Store and document embeddings
- Langchain and GPT4
- Streamlit
- Docker, Bash, Pytest, Poetry and more

## Running the app

### Setup

To run this project you need a system where you can run bash scripts and Linux type commands in your terminal. You also need Git and Docker. See the official docs for instructions on how to install them. 

You also need an account with an API key at OpenAI. Unless you have free credits to use **running this app will cost money**. As a reference my total cost when developing this project added up to around $7. Buying $2 or $3 of credits should be plenty enough to try the app out.

Once you have an API key, paste it into the file `.env.example` and rename the file just `.env`. Like so:

```
OPENAI_API_KEY=YourKey123
```

Remember not to share your API key with anyone!

#### Resources:

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://docs.docker.com/get-docker/)
- [OpenAI](https://chat.openai.com)

### Download the Github repository and start a app-container

With the tools in place, download the repository.
```
$ git clone https://github.com/erikgrip/langchain_docs_chatbot.git
```

To build a docker image and run the app in a container, navigate to the project directory and run:

```bash
bash ./docker/run.sh
```

You can then interact with the app at `http://0.0.0.0:8501` using a web browser.

### App config

The start up scrips takes the following options:

- --build : re-build docker image
- -f, --force_data_download : download langchain repo again
- -d, --delete_persisted_db : delete any previosly created vector store
- -n, --num_retrieved_docs : number of items to retrive from vector store to answer question
- -t, --temperature : the temperature parameter to use for GPT4

For example:

```bash
# Scrap your previous vector store index to create a new one,
# and make GPT4 use 0.5 as value for temperature.
bash ./docker/run.sh -d --temperature 0.5
```

## Development Setup

Download the repo and navigate to the project directory. Then install pyenv ([instructions](https://github.com/pyenv/pyenv#installation)) and run:

```bash
pyenv install 3.10.6
pyenv local 3.10.6
```

Install poetry in current python version:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then install the dependencies with:

```bash
poetry install --with dev
```
