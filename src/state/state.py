from typing import TypedDict, List
from langchain_core.messages import BaseMessage
from langchain.schema import Document  # keep as you have

class GraphState(TypedDict):
    question: str
    answer: str
    web_search: bool
    documents: List[Document]
    messages: List[BaseMessage]