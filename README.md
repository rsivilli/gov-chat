# Gov Chat

A simple chatbot for answering questions about a website's content.

## Objectives

- Provide a deployable service 
- Configurable for either chatgpt or a privately hosted LLM
- Provide a local test harness


## Setup 

The project is based in python and is managed by poetry. 

Install python 3.10 according to your operating system and following the instructions here for installing poetry [here](https://python-poetry.org/docs/)

Once you have python and poetry installed, you should be able to run `poetry install` at the root of the repo and all dependencies will be grabbed. 


## Install LLM

Pick a model from the list [here](https://gpt4all.io/index.html)

Create a folder "models" and place the LLM there. Currently, only tested with `ggml-gpt4all-j-v1.3-groovy.bin`


## Running Test GUI

running the command `python ./test_gui/app.py` will spin up a service listening at http://127.0.0.1:7860. Click on the link or copy/paste into your browser