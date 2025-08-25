#===============================================================================
#  File Name    : gmail_agent.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-08-22
#  Last Updated : 2025-08-22
#  Version      : v1.0.0

#  Language     : Python
#  File name    : gmail_agent.py
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
from abc import abstractmethod, ABC
import sys
sys.path.append('.')
from dotenv import load_dotenv
load_dotenv(".env")

from langgraph.prebuilt import create_react_agent
from playwright.sync_api import sync_playwright
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

from src.infrastructure.llm.gemini_llm import GeminiLLM
from tools.mail_tool import view_unread_messages_from_sender, list_unread_messages, list_unread_messages_from_sender
from src.infrastructure.llm.tts import HumanSpeaker, AgentSpeaker


class GmailBaseAgent(ABC):
    def __init__(self):
        self.gllm = GeminiLLM()
        self.llm = self.gllm.get_chat_llm()
        self.page = None
        self.system_prompt = """you are a Gmail Agent. Your job is to 
        1. get the unread messages from a specific sender, read them and summarize them in  detailed manner one by one using tool `get_unread_messages_from_sender`. 
        2. If the user wants to get the list of unread messages, give the sender name and read the subject of the message `get_unread_messages_list`.
        3. If the user wants to get the list of unread messages from a specific sender, give the sender name and read the subject of the message `get_unread_messages_list_from_sender`.
        """
        self.human_speaker = HumanSpeaker()
        self.agent_speaker = AgentSpeaker()
        
    @tool
    def get_unread_messages_from_sender( sender):
        """
            Tool to retrieve message from sender
        """
        mails  = view_unread_messages_from_sender(sender)
        if len(mails) > 0:
            return mails
        else:
            return "No messages found"
        
    @tool
    def get_unread_messages_list():
        """
            Tool to retrieve message from sender
        """
        mails  = list_unread_messages()
        if len(mails) > 0:
            return mails
        else:
            return "No messages found"
        
    @tool
    def get_unread_messages_list_from_sender( sender : str):
        """
            Tool to retrieve list message from sender
        """
        mails  = list_unread_messages_from_sender(sender)
        if len(mails) > 0:
            return mails
        else:
            return "No messages found"
        
    def get_agent(self):
        tools = [GmailBaseAgent.get_unread_messages_from_sender, 
                 GmailBaseAgent.get_unread_messages_list,
                 GmailBaseAgent.get_unread_messages_list_from_sender
                 ]
        memory = MemorySaver()
        agent = create_react_agent(self.llm, 
                                   prompt=self.system_prompt,
                                   tools=tools,
                                   checkpointer=memory
                                   )
        return agent
    
    def main( self , text: str ):
        agent = self.get_agent()
        input_message = {
        "role": "user",
        "content": text,
        }
        last_ai_message = None
        config = {"configurable": {"thread_id": "abc123"}}
        for step in agent.stream(
            {"messages": [input_message]},
            config=config,
            stream_mode="values",
                ):
            try:
                step["messages"][-1].pretty_print()
                msg = step["messages"][-1]
                if getattr(msg, "type", None) == "ai" or getattr(msg, "role", None) == "assistant":
                    last_ai_message = msg.content.strip()
                    # self.agent_speaker.speak(content)
                    
            except Exception as e:
                print(e)
                print( step )
        return  last_ai_message
                
if __name__ == "__main__":
    text = "get mail from daily dose of DS"
    agent = GmailBaseAgent()
    agent.main(text)