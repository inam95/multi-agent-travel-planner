from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from app.agents.prompts import (
  REQUIREMENTS_AGENT_SYSTEM_PROMPT,
  PLANNER_AGENT_SYSTEM_PROMPT,
  BOOKER_AGENT_SYSTEM_PROMPT
  )
from app.agents.response_models import (
  RequirementsAgentResponseModel,
  PlannerAgentResponseModel,
  BookerAgentResponseModel
  )
from app.agents.tools import (
  search_flight_availability,
  web_search,
  book_flight,
  book_hotel,
  search_hotels
  )
from app.core import llm


requirements_agent = create_agent(
  model=llm,
  tools=[search_flight_availability],
  system_prompt=REQUIREMENTS_AGENT_SYSTEM_PROMPT,
  response_format=ToolStrategy(RequirementsAgentResponseModel))

planner_agent = create_agent(
  model=llm,
  tools=[web_search],
  system_prompt=PLANNER_AGENT_SYSTEM_PROMPT,
  response_format=ToolStrategy(PlannerAgentResponseModel))

booker_agent = create_agent(
  model=llm,
  tools=[book_flight, book_hotel, search_hotels],
  system_prompt=BOOKER_AGENT_SYSTEM_PROMPT,
  response_format=ToolStrategy(BookerAgentResponseModel))




if __name__ == "__main__":
  for chunk in requirements_agent.stream(
    input={"messages": ["I want to travel to Seoul(ICN) from Tokyo(NRT) My days are flexible."]},
    stream_mode="updates",
  ):
    print(chunk)