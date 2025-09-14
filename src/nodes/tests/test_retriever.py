from src.nodes.retrieval import retrieve
from src.state.state import GraphState
from dotenv import load_dotenv


def test_retriever():
    question = "What medicine is used for suspected Salmonella"
    state = GraphState()
    state["question"] = question
    result = retrieve(state)

    print("Retrieved documents:", result["documents"])
    print("Original question:", result["question"])

# ----- Run tests -----
if __name__ == "__main__":
    test_retriever()