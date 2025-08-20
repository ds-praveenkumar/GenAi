#===============================================================================
#  File Name    : Broadband_bill_gent.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-08-20
#  Last Updated : 2025-08-20
#  Version      : v1.0.0

#  Language     : Python
#  File name    : Broadband_bill_gent.py
#  Dependencies : 
#    - Dependency 1
#    - Dependency 2

#  Inputs       : Expected inputs
#  Outputs      : Expected outputs
#  Usage        : 
#    Example usage

#  Notes        : 
#    - Notes or TODOs
#===============================================================================
import sys
sys.path.append('.')

from langgraph.prebuilt import create_react_agent
from playwright.sync_api import sync_playwright
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

from src.infrastructure.llm.gemini_llm import GeminiLLM
from tools.browser_use import download_file, rail_wire_login

SYSTEM_PROMPT = """
You are an expert in browser use and can surf internet.
Your job is to use tool to download broadband bill.
"""

@tool
def get_broadband_bill():
    """
    Download broadband bill
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        rail_wire_login(page)
        context.close()
        browser.close()
    return "bill.pdf downloaded successfully"

tools = [get_broadband_bill]
gllm = GeminiLLM()
llm= gllm.get_chat_llm()
memory = MemorySaver()
agent = create_react_agent(llm, 
                           prompt=SYSTEM_PROMPT,
                           tools=tools,
                           checkpointer=memory
                           )

if __name__ == "__main__":
    input_message = {
    "role": "user",
    "content": "Download broadband bill",
}
    config = {"configurable": {"thread_id": "abc123"}}
    for step in agent.stream(
        {"messages": [input_message]},
        config=config,
        stream_mode="values",
            ):
        try:
            step["messages"][-1].pretty_print()
        except Exception as e:
            print(e)
            print( step )
