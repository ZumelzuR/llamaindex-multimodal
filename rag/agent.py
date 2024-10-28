from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from rag.tools.image_tools import setup_tools

REACT_AGENT_PROMPT = f""" 
                Agent that will answer general question regarding ikea manuals, 
                not use any prior knowledge, only answer from documents or other agents. 
                First call get_product_list_tool tool to check if the user is asking about an product of the list.
                If you dont find a product item by the query, you can go to check the list of products using your tools and then figure the item, but if you think as a typo error, but if is completely different product that is not in the list, you can ask to the user that you don't have that item. 
                If you can't answer, ask more information to the user.
                Always try to figure out if the user wanted to answer about a product on the list, so if he mistake with the name of the product try to figure out wich ones he wants using the get_product_list_tool.
                Always answer in the language the main user talk to you initially
                """


def init_agent():
    llm = OpenAI(model="gpt-3.5-turbo")
    agent = ReActAgent.from_tools(
        [*setup_tools()],
        llm=llm,
        verbose=True,
        system_prompt=REACT_AGENT_PROMPT,
    )
    return agent


agent = init_agent()


def message(query) -> str:
    response = agent.chat(query)
    return str(response)
