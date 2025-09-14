from typing import TypedDict, List, Literal
from langchain_core.messages import BaseMessage
from langchain.schema import Document  # keep as you have

class GraphState(TypedDict):
    question: str
    answer: str
    web_search: bool
    user_id: str
    documents: List[Document]
    messages: List[BaseMessage]
    route: Literal["messages", "vectorstore", "websearch"]