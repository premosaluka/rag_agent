from dotenv import load_dotenv

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
import CONFIG as C
from src.nodes import *
from src.state.state import GraphState

load_dotenv()

### NODES
workflow = StateGraph(GraphState)

# Memory nodes
workflow.add_node("MEMORY_READ", read_memory_node)
workflow.add_node("MEMORY_WRITE", write_memory_node)

workflow.add_node("ROUTER",route_query_node)
workflow.add_node("RETRIEVE",retrieve)
workflow.add_node("WEBSEARCH",web_search)
workflow.add_node("GENERATE",generate)

### EDGES
#workflow.add_edge(START, "ROUTER")
workflow.add_edge(START, "MEMORY_READ")
workflow.add_edge("MEMORY_READ", "ROUTER")

workflow.add_conditional_edges(
    "ROUTER",
    lambda state: state["route"],  # get route from state
    {
        "messages": "GENERATE",
        "vectorstore": "RETRIEVE",
        "websearch": "WEBSEARCH",
    }
)

workflow.add_edge("WEBSEARCH", "GENERATE")
workflow.add_edge("RETRIEVE", "GENERATE")
#workflow.add_edge("GENERATE", END)
workflow.add_edge("GENERATE", "MEMORY_WRITE")
workflow.add_edge("MEMORY_WRITE", END)

# app = workflow.compile()
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

if __name__ == '__main__':
    # app.get_graph().draw_mermaid_png(output_file_path="agent.png")
    # Example initial state
    state = {
        "question": "WHat is blue tongue ?",
        "answer": "",           # empty for now, agent will fill
        "web_search": False,
        "documents": [],        # optional
        "messages": [],         # memory will be filled
        "user_id": "user123"    # required for memory nodes
    }

    # Invoke the workflow
    result_state = app.invoke(state,
                              config={"configurable": {"thread_id": "user-123"}})

    # Check the result
    print("Final state:", result_state)

    result_state = app.invoke({"question":"What was the previous topic?"},
                              config={"configurable": {"thread_id": "user-123"}})



    # Check the result
    print("Final state:", result_state)

    print('finally over')