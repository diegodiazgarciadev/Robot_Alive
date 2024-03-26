import logging
from src.callbacks.tool_callbacks import AgentCallbackHandler
import warnings
from src.tools.tools import move_and_pic
from langchain.agents import initialize_agent, AgentType
from langchain_openai import OpenAI
from config.config import OPENAI_API_KEY
warnings.filterwarnings("ignore", category=DeprecationWarning, message="LangChainDeprecationWarning")


def goal_agent(goal: str) -> str:
    """
     you are a robot with the capacity of doing some movements and sometimes you set a gaol like find something, explore
     or get close and object.
     Usually this goal is not direct so you need to do more than one action.
     with this agent you will be able to take pictures of your environment, read some sensor and act in consequence
    :param goal: it is an text where is explained what is the next goal to achieve
    :return: result of the agent
    """

    try:
        logging.info("Initializing the LLM agent.")
        llm = OpenAI(temperature=0,api_key = OPENAI_API_KEY, callbacks=[AgentCallbackHandler()])

        tools = [move_and_pic]

        agent = initialize_agent(tools,
                                 llm,
                                 agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                 max_iterations=5,
                                 verbose=True,
                                 )

        logging.info(f"Running the agent with goal: {goal}")
        result = agent.run(goal)
        logging.info("Agent run completed successfully.")

        return result
    except Exception as e:
        logging.exception(f"An error occurred while running the agent: {e}")
        raise