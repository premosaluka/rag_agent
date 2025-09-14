from typing import Any, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from src.state.state import GraphState

from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the provided context to answer the user's question."),
    ("human", "Question: {question}\n\nContext:\n{context}"),
    ("ai", "Answer:")
])

generation_chain = prompt | llm | StrOutputParser()

def generate(state: GraphState, use_documents=True) -> Dict[str, Any]:
    print("---generate---")
    question = state["question"]
    documents = state["documents"]
    messages = state.get("messages", [])


    # Extract text from documents
    if isinstance(documents, list) and use_documents:
        context_str = "\n\n".join(
            [doc.page_content if hasattr(doc, "page_content")
             else str(doc) for doc in documents]
        )
    else:
        context_str = str(documents)

    # Add last N messages to context.
    if messages:
        last_messages = messages[-3:]
        history_str = "\n\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in last_messages])
        context_str = f"{context_str}\n\nConversation history:\n{history_str}"

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"question": question, "context": context_str})

    # Append question/answer to messages
    messages.extend([
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer}
    ])

    return {
        "documents": documents,
        "question": question,
        "answer": answer,
        "messages": messages
    }