from dotenv import load_dotenv
load_dotenv()

import CONFIG as C
from typing import Any, Dict
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults

from src.state.state import GraphState

web_search_tool = TavilySearchResults(k=C.K_TAVILY_SEARCH_RESULTS)

def web_search(state: GraphState) -> Dict[str, Any]:
    question = state["question"]
    documents = state["documents"]
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    documents.append(web_results)
    return {"documents": documents, "question": question}