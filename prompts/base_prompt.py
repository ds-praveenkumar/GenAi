#===============================================================================
#  File Name    : base_prompt.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-07-17
#  Last Updated : 2025-07-17
#  Version      : v1.0.0

#  Language     : Python
#  File name    : base_prompt.py
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

from abc import ABC, abstractmethod
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

class BasePrompt(ABC):
    def __init__(self, prompy_type, prompt) :
        self.prompt_type = prompy_type
        self.prompt = prompt
        
    def __repr__(self) -> str:
        return f"{self.prompt_type}"
    
    def _get_simple_prompt(self, ):
        prompt_template = PromptTemplate.from_template(
            template=self.prompt
        )
        return prompt_template
    
    @abstractmethod
    def _get_chat_prompt(self, query):
        chat_template = ChatPromptTemplate.from_messages([
            ("system", self.prompt),
            ("human", query)
            
        ])
        return chat_template
    