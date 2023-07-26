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


## Current repo state


|-- customer_management - primary logic and models around individual customers and their respective chatbots. Used primarily by django, but models and access mechanisms are used by some thigns in gov_chat
|-- /frontend - teststub for js client and example implementation for a user facing chatbot
|-- /gov_chat - broken out funcitonal components for all work around the actual chatbot and lifecycle therein
|-- /gov_chat_management - base thing of django project
|-- /test_gui - gradio project for testing that the individual steps in gov_chat worked in the proof of concept


## TODO 

 - [ ] create dockerfile for management
 - [ ] update docker-compose to spin up django for management
 - [ ] create dockerfiles for primary functions (eg sitemap-gen, site-indexing)
 - [ ] migrate chat service to fastapi