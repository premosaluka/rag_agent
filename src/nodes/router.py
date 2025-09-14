from typing import Literal
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

load_dotenv()

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource or use the conversation context."""
    datasource: Literal["messages", "vectorstore", "websearch"] = Field(
        ...,
        description=(
            "Decide the best source to answer the user question. "
            "'messages' = use conversation context if it contains enough information, "
            "'vectorstore' = query the knowledge base if the question relates to stored documents, "
            "'websearch' = use an online search if the question needs up-to-date or external information."
        ),
    )

llm = ChatOpenAI(model="gpt-4", temperature=0)
structured_llm_router = llm.with_structured_output(RouteQuery)

system = """
You are an expert at routing a user question to the correct source.

Rules for choosing:
1. If the user explicitly specifies which source to use in the question (messages, vectorstore, or websearch), always respect that.
2. Otherwise:
   - "messages": Use the conversation history if it contains enough context to answer the question directly.
   - "vectorstore": The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks. 
     Use it for questions on those topics if they are not fully answerable from the conversation history.
   - "websearch": Use web search for all other topics or if the question requires up-to-date external information.

Always choose the single best source.
"""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Conversation so far:\n{messages}\n\nLast question:\n{question}"),
    ]
)

question_router = route_prompt | structured_llm_router

def route_query_node(state: dict) -> dict:
    """
    Calls the LLM router to decide which datasource to use.
    Returns a dict with the router output merged into the state.
    """
    # Make sure messages exist
    messages = state.get("messages", [])

    # Invoke the structured LLM router
    router_result = question_router.invoke({
        "messages": messages,
        "question": state.get("question", "")
    })

    # router_result is a RouteQuery object with 'datasource'
    # Return as dict so LangGraph merges it correctly
    return {"route": router_result.datasource}