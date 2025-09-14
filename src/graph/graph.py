from dotenv import load_dotenv

from langgraph.graph import START, END, StateGraph
import CONFIG as C
from src.nodes import *
from src.state.state import GraphState

load_dotenv()

def route_decision(state):
    # call the structured LLM once
    result = question_router.invoke(state)
    return result.datasource

### NODES
workflow = StateGraph(GraphState)
workflow.add_node("ROUTER",route_decision)
workflow.add_node("RETRIEVE",retrieve)
workflow.add_node("WEBSEARCH",web_search)
workflow.add_node("GENERATE",generate)

### EDGES
workflow.add_edge(START, "ROUTER")
workflow.add_conditional_edges(
    "ROUTER",
    lambda datasource: datasource,
    # path map
    {
        "messages": "GENERATE",
        "vectorstore": "RETRIEVE",
        "websearch": "WEBSEARCH",}
)

workflow.add_edge("WEBSEARCH", "GENERATE")
workflow.add_edge("RETRIEVE", "GENERATE")
workflow.add_edge("GENERATE", END)


app = workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path="agent.png")
