RAG Agent with LangGraph & ChromaDB
✈️
Overview

This project is an experimental Retrieval-Augmented Generation (RAG) system powered by LangGraph.
The agent dynamically decides how to answer user questions by:

Querying a ChromaDB vector store (knowledge base)

Performing a web search if local knowledge is insufficient (Tavily)

Using recent conversation history (messages) when context is enough

Currently, the project is in its initial development stage.


What I want to test further in the future:

Long term memory store

Streamlit – frontend

FastAPI – API deployment
