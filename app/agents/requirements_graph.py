import json
from typing import Optional
from langchain.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

from app.agents import requirements_agent

checkpointer = InMemorySaver()

class RequirementsGraphState(MessagesState):
  requirements_complete: bool
  interruption_message: str
  requirements: Optional[dict]

def requirements_agent_node(state: RequirementsGraphState) -> RequirementsGraphState:
  response = requirements_agent.invoke({"messages": state["messages"]})

  response = response["structured_response"]
  requirements_response = response.requirements
  question = requirements_response.missing_info.question

  if question != "":
    return {
      "messages": [
        AIMessage(content=question)
      ],
      "requirements_complete": False,
      "interruption_message": question,
      "requirements": None
    }

  return {
    "messages": [],
    "requirements_complete": True,
    "interruption_message": "",
    "requirements": requirements_response.model_dump()
  }


def should_ask_user_for_info(state: RequirementsGraphState) -> bool:
  return not state["requirements_complete"]


def ask_user_for_info(state: RequirementsGraphState) -> RequirementsGraphState:
  user_response = interrupt(state["interruption_message"])

  return {
    "messages": [
      HumanMessage(content=user_response)
    ],
    "requirements_complete": False,
    "interruption_message": "",
    "requirements": None
  }


graph = StateGraph(RequirementsGraphState)
graph.add_node("requirements_agent", requirements_agent_node)
graph.add_node("ask_user_for_info", ask_user_for_info)
graph.add_edge(START, "requirements_agent")
graph.add_conditional_edges("requirements_agent", should_ask_user_for_info, {
  True: "ask_user_for_info",
  False: END
})
graph.add_edge("ask_user_for_info", "requirements_agent")

requirements_graph = graph.compile(checkpointer=checkpointer)



if __name__ == "__main__":
  initial_state = RequirementsGraphState(
    messages=[
      HumanMessage(
          content="I want to go to Seoul(ICN) from Tokyo(NRT). My dates are flexible."
      )
    ],
    requirements_complete=False,
    interruption_message=""
  )

  config = {"configurable": {"thread_id": "thread-1"}}
  result = requirements_graph.invoke(initial_state, config=config)

  while True:
    if "__interrupt__" in result:
      print(result["__interrupt__"])
      user_input = input("")
      current_state = Command(resume=user_input)

      result = requirements_graph.invoke(current_state, config=config)
    else:
      break

  print(result["requirements"])
