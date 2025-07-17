#===============================================================================
#  File Name    : simple_prompt.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-07-17
#  Last Updated : 2025-07-17
#  Version      : v1.0.0

#  Language     : Python
#  File name    : simple_prompt.py

#===============================================================================
import sys
sys.path.append('.')
from src.infrastructure.llm.gemini_llm import GeminiLLM
from base_prompt import BasePrompt
from utils.utils import print_console, show


class SimplePrompt( BasePrompt ):
    
    def __init__(self, query):
        self.prompt = "You are a simple Answering Bot. Answer the query asked by the user query: {query}"
        self.prompt_type = "simple prompt"
        super().__init__(self.prompt_type, self.prompt)
        self.query= query
        
    def _get_chat_prompt(self):
        return super()._get_chat_prompt(self.query)
    
if __name__ == '__main__':    
    query = "An instrument store gives a 10% discount to all students off the original cost of an instrument. During a back to school sale an additional 15% is taken off the discounted price. Julie, a student at the local high school, purchases a flute for $306. How much did it originally cost?"
    prompt = SimplePrompt(query)
    gllm = GeminiLLM()
    llm = gllm.get_chat_llm()
    chain = prompt._get_simple_prompt() | llm
    chat_chain = prompt._get_chat_prompt() | llm
    res = chat_chain.invoke({"query": query })
    show( f"\n{prompt.prompt_type}\n", "bold magenta")
    show(f"{res.content}\n", "green")
