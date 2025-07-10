from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


os.environ["GOOGLE_API_KEY"]=""

class GeminiLLM:
    def __init__( self ):
        self.model = "gemini-2.0-flash",
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