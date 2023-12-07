# langchain-docs-chatbot
Create a chatbot app to answer questions about langchain based on the langchain documentation.

# motion_title_generator

## Table of contents

- [General info](#general-info)
- [Technologies](#technologies)
- [Running the app](#running-the-app)
- [Development Setup](#development-setup)


## General info

This is a project to build a chatbot app, that can answer questings about hte python package langchain. The app was built using OpenAI's GPT4 in the autumn of 2023. Even though the model itself was not aware of langchain at the time due to its lknowledge cutoff, the app can search information about langchain from a vector store that was loaded with the markdown filed from langchain's Github repo.


> **User:**
>> What is the purpose of langchain?
>
> **Assistant:**
>> It appears that there might be some confusion about the term "langchain". As of now, there is not enough information available specific to a tool, technology, or platform named "Langchain". The term may have been misspelled or misunderstood. If it's related to programming, blockchain, or any other specific field, please provide additional context for a more accurate answer.
>
> --  _GPT4, 7 December 2023_


What interaction with the app looks like:


<video width="500" height="500" controls>
  <source src="resources/app_demo.mp4" type="video/mp4">
</video>


## Technologies

The project was created using

- Python
- Vector Store and document embeddings
- Langchain and GPT4
- Streamlit
- Docker, Bash, Pytest, Poetry and more


## Running the app

To run this project you need a system where you can run bash scripts and Linux type commands in your terminal. You also need Git and Docker. See the official docs for instructions on how to install them. With the tools in place, clone the repository using a local terminal.

You need an account att OpenAI with an API key. Unless you have free credits to use, **running this app will cost money**. You'll be responsible for your own costs but as a reference my total cost when developing this project added up to around $7. Just trying it out should be substantially less.

TODO: API KEY

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://docs.docker.com/get-docker/)

```
$ git clone https://github.com/erikgrip/langchain_docs_chatbot.git
```

To build a docker image and run the app in a container, navigate to the project directory and run:

```bash
bash ./docker/run.sh
```
You can the interact with the app at `http://0.0.0.0:8501` using a web browser. 

The start up scrips takes the following options:
* --build : re-build docker image
* -f, --force_data_download : download langchain repo again
* -d, --delete_persisted_db : delete any previosly created vector store
* -n, --num_retrieved_docs : number of items to retrive from vector store to answer question
* -t, --temperature : the temperature parameter to use for GPT4



## Development Setup


## Cleaning up
