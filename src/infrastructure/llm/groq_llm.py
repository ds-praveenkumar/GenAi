#===============================================================================
#  File Name    : groq_llm.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-08-22
#  Last Updated : 2025-08-22
#  Version      : v1.0.0

#  Language     : Python
#  File name    : groq_llm.py
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
from langchain_groq import ChatGroq

import sys
sys.path.append('.')
from dotenv import load_dotenv
import os
load_dotenv(".env")

api_key=os.getenv("GROQ_API_KEY")
print(api_key)

if not api_key:
    raise EnvironmentError("GROQ_API_KEY is not set in environment variables.")
class GroqLLM:
    def __init__( self ):
        self.model = "llama-3.1-8b-instant",
        self.temperature=0,
        self.max_tokens=2047,
        self.timeout=None,

    def get_chat_llm( self ):
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=2047,
            timeout=None,
        )
        
        return llm
        
if __name__ == '__main__':
    gllm = GroqLLM()
    llm = gllm.get_chat_llm()
    response = llm.invoke("What is flash attention?")
    print(f'response: {response.content}')