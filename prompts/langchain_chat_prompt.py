import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from llm.gemini_llm import GeminiLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
import asyncio
from utils.utils import show

class PromptTemplates:
    def __init__(self) -> None:
        self.gllm = GeminiLLM()
        self.llm = self.gllm.get_chat_llm()
    
    def chat_template(self  ):
        """
            chat template data
        """
        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template('you are a Helpful {agent} assistant'),
            HumanMessagePromptTemplate.from_template('Ask you query: {user_query}')            
        ])
        return prompt_template
    
    def get_chain(self ):
        """
            create llm chain with the prompt template
        """
        llm_chain = self.chat_template() | self.llm 
        return llm_chain
    
    async def call_llm(self, **kwargs) :
        """
            call llm with the input values
        """
        llm_chain = self.get_chain()
        response  = await llm_chain.ainvoke(kwargs)
        show(response.content)
        return response.content
    
if __name__ == '__main__':
    pt = PromptTemplates()
    asyncio.run(pt.call_llm(agent='AI', user_query='what is flash attention?')) 
    