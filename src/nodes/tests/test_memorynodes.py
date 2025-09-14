from src.nodes.memory_node import db
from src.nodes.memory_node import write_memory_node


# Example state
state = {
    "user_id": "user123",
    "question": "What is my favorite color?",
    "answer": "Your favorite color is blue."
}

# Write messages using the node
state = write_memory_node(state)

# Check messages were added
messages = db.all()
for msg in messages:
    print(f"{msg['timestamp']} | {msg['user_id']} | {msg['role']} | {msg['content']}")