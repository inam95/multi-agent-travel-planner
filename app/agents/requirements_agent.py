from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from app.agents.prompts import REQUIREMENTS_AGENT_SYSTEM_PROMPT
from app.agents.response_models import RequirementsAgentResponseModel
from app.agents.tools import search_flight_availability
from app.core import llm


agent = create_agent(model=llm, tools=[search_flight_availability], system_prompt=REQUIREMENTS_AGENT_SYSTEM_PROMPT, response_format=ToolStrategy(RequirementsAgentResponseModel))

if __name__ == "__main__":
  for chunk in agent.stream(
    input={"messages": ["I want to travel to Seoul(ICN) from Tokyo(NRT) My days are flexible."]},
    stream_mode="updates",
  ):
    print(chunk)

