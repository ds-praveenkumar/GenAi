from llm.gemini_llm import GeminiLLM

gllm = GeminiLLM()
llm = gllm.get_chat_llm()

print(llm.invoke('hi').content)