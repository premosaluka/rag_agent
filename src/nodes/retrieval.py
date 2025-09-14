from typing import TypedDict, Any, Dict
from src.state.state import GraphState
from vectorstore.vectorstore import retriever

def retrieve(state: GraphState) -> Dict[str, Any]:
    question = state["question"]
    # do semantic search and get all relevant docs
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question,}