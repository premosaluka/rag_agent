from src.nodes.router import question_router
from dotenv import load_dotenv


def test_router():
    messages = [
        {"role": "user", "content": "How do I fine-tune a GPT model?"},
        {"role": "assistant", "content": "You can fine-tune GPT using OpenAI's API or LoRA."},
    ]

    test_cases = [
        ("Is my last conversation enough to answer this?", "messages"),
        ("What is the latest news on AI. Use websearch.", "websearch"),
        ("What's the latest news on GPT-5?", "websearch"),
    ]

    for question, expected in test_cases:
        result = question_router.invoke({"messages": messages, "question": question})
        print(f"Question: {question}")
        print(f"Predicted datasource: {result.datasource}, Expected: {expected}")
        print("-" * 40)

# ----- Run tests -----
if __name__ == "__main__":
    test_router()