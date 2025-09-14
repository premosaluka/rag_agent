from typing import List
from langchain.schema import BaseMessage, HumanMessage, AIMessage, Document
from datetime import datetime
from tinydb import TinyDB, Query
from dotenv import load_dotenv
from typing import TypedDict, Any, Dict
from src.state.state import GraphState
import os

import CONFIG as C

load_dotenv()

# Here we store the memory
memory_path = os.path.join(C.MEMORY_DB_FOLDER, "memory_store.json")
db = TinyDB(memory_path)
Message = Query()

#--------------------------------------------------------------------------#
##------------------------ Nodes ------------------------------------------#
#--------------------------------------------------------------------------#

def read_memory_node(state: GraphState) -> Dict[str, Any]:
    user_id = state.get("user_id")

    # No user - no memory
    if not user_id:
        #state["messages"] = []
        return {"messages":[]}

    # Fetch last N messages for this user
    messages_data = db.search(Message.user_id == user_id)
    if not messages_data:
        #state["messages"] = []
        return {"messages":[]}

    # Sort by timestamp and take most recent N
    messages_data = sorted(
        messages_data, key=lambda x: x.get("timestamp", ""), reverse=True
    )[:C.MEMORY_NR_RECENT_MSGS]

    # Convert to BaseMessage objects
    messages: List[BaseMessage] = []
    for msg in reversed(messages_data):  # reverse so oldest comes first
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        else:
            messages.append(AIMessage(content=content))

    #state["messages"] = messages
    print(state)
    return {"messages": messages}


def write_memory_node(state: GraphState) -> Dict[str, Any]:
    user_id = state.get("user_id")
    if not user_id:
        return {}

    # Store user message
    db.insert({
        "user_id": user_id,
        "role": "user",
        "content": state["question"],
        "timestamp": datetime.now().isoformat()
    })

    # Store assistant message
    db.insert({
        "user_id": user_id,
        "role": "assistant",
        "content": state["answer"],
        "timestamp": datetime.now().isoformat()
    })

    return {}
