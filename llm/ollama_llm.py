from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.utils import show

class OllamaModel:
    def __init__(self):
        self.model_name = 'llama3.1'
        self.llm = OllamaLLM(model="llama3.1",temperature=0.1,  num_ctx=2048)
        
    def call_llm( self, text ):
        response  = self.llm.invoke(text)
        show( response )
        return response
    
if __name__ == '__main__':
    ollama = OllamaModel()
    ollama.call_llm('what is flash attention')