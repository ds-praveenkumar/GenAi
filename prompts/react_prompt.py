#===============================================================================
#  File Name    : react_prompt.py
#  Project Name : Project Name
#  Description  : 
#    React Prompt

#  Author       : Praveen Kumar
#  Created On   : 2025-07-17
#  Last Updated : 2025-07-17
#  Version      : v1.0.0

#  Language     : Python
#  File name    : react_prompt.py
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
from src.infrastructure.llm.gemini_llm import GeminiLLM
from base_prompt import BasePrompt
from utils.utils import print_console, show

class REACTPrompt( BasePrompt ):
    def __init__( self , query ):
        self.prompt = '''
            To solve the task, you must plan forward to proceed in a series of steps, in a cycle of 'Thought:', 'Action:', and 'Observation:' sequences.
            At each step, in the 'Thought:' sequence, you should first explain your reasoning towards solving the task, then the tools that you want to use.
            Then in the 'Action:' sequence, you shold use one of your tools.
            During each intermediate step, you can use 'Observation:' field to save whatever important information you will use as input for the next step.
            query: {query}
            '''
        self.prompt_type = "REACT"
        self.query = query
        
    def _get_chat_prompt(self ):
        return super()._get_chat_prompt(self.query)
    
if __name__ == '__main__':    
    query = "An instrument store gives a 10% discount to all students off the original cost of an instrument. During a back to school sale an additional 15% is taken off the discounted price. Julie, a student at the local high school, purchases a flute for $306. How much did it originally cost??"
    prompt = REACTPrompt(query)
    gllm = GeminiLLM()
    llm = gllm.get_chat_llm()
    chain = prompt._get_simple_prompt() | llm
    chat_chain = prompt._get_chat_prompt() | llm
    res = chat_chain.invoke({"query": query })
    show( f"\n{prompt.prompt_type}\n", "bold magenta")
    show(f"{res.content}\n", "green")
