import sys
sys.path.append('.')
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv(".env")

api_key=os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise EnvironmentError("GOOGLE_API_KEY is not set in environment variables.")
class GeminiLLM:
    def __init__( self ):
        self.model = "gemini-2.5-flash",
        self.temperature=0,
        self.max_tokens=2047,
        self.timeout=None,

    def get_chat_llm( self ):
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=2047,
            timeout=None,
        )
        
        return llm
        
if __name__ == '__main__':
    gllm = GeminiLLM()
    llm = gllm.get_chat_llm()
    response = llm.invoke("What is flash attention?")
    print(f'response: {response.content}')