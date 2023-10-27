## Introduction

The aim of this project is to use LLM in a custom manner. LLM have been trained on a large amount of data. However must of the case, when we want to adapt them to a corporation, to our own documentation or even to recent informations published on the web, we are limited.

This is where the RAG (retrieval augmented generation) comes into play 🪄

RAG allows LLM to be updated with new infotmations without being retrained.

<a href="https://www.youtube.com/watch?v=T-D1OfcDW1M" target="_blank">
    <img src="img/whatisragvideo.jpeg" width="60%" alt="Vidéo YouTube">
</a>


## Architecture

```mermaid

flowchart LR
comment f
A[Hard] -->|Text| B(Round)
B --> C{Decision}
C -->|One| D[Result 1]
C -->|Two| E[Result 2]
```