from src.nodes.websearch import web_search
from src.state.state import GraphState
from dotenv import load_dotenv

def test_retriever():
    question = "What medicine is used for suspected Salmonella in cattle"
    state = GraphState()
    state["question"] = question
    result = web_search(state)

    print("Retrieved documents:", result["documents"])
    print("Original question:", result["question"])

# ----- Run tests -----
if __name__ == "__main__":
    test_retriever()