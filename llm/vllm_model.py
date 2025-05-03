from vllm import LLM

class VLLMModel:
    def __init__(self) :
        self.model_id = 'Qwen/Qwen2.5-1.5B'
        self.llm = LLM(model=self.model_id)

    def call_llm( self, text:str):
        output = self.llm.generate(text)
        print( output)
        return output

if __name__ == '__main__':
    vllm = VLLMModel()
    vllm.call_llm('hi')