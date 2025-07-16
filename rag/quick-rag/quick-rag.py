#/**
# * ====================================================
# * @file        quick-rag.py
# * @author      Praveen Kumar
# * @created     2025-07-10
# * @last updated 2025-07-10
# * @version     1.0.0
# *
# * @description quick-rag
# *
# * @usage       python quick-rag.py
# * @dependencies None
# *
# * @license     MIT
# * ====================================================
# */

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
import warnings
warnings.filterwarnings("ignore")

class RAGPipelineBuilder:
    def __init__(self):
        self.document_path = None
        self.chunk_size = 650
        self.chunk_overlap = 50
        self.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        self.llm_model = "mistralai/Mistral-7B-Instruct-v0.3"
        self.docs = None
        self.split_docs = None
        self.vectorstore = None
        self.retriever = None
        self.llm = None
        self.qa_chain = None

    def load_documents(self, path: str):
        self.document_path = path
        loader = TextLoader(path)
        self.docs = loader.load()
        return self

    def split_documents(self):
        splitter = CharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        self.split_docs = splitter.split_documents(self.docs)
        return self

    def embed_documents(self):
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model, model_kwargs={"device": "cuda"})
        self.vectorstore = FAISS.from_documents(self.split_docs, embeddings)
        return self

    def create_retriever(self):
        self.retriever = self.vectorstore.as_retriever()
        return self

    def load_llm(self):
        hf_pipeline = pipeline(
            "text2text-generation",
            model=self.llm_model,
            tokenizer=self.llm_model,
            max_length=256,
            temperature=0,
        )
        self.llm = HuggingFacePipeline(pipeline=hf_pipeline)
        return self

    def build_qa_chain(self):
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, retriever=self.retriever)
        return self

    def run_query(self, query: str) -> str:
        if not self.qa_chain:
            raise ValueError("QA Chain not built. Call build_qa_chain() before running a query.")
        return self.qa_chain.run(query)


# === Usage ===
if __name__ == "__main__":
    builder = RAGPipelineBuilder()
    response = (
        builder
        .load_documents("/home/praveen/Desktop/git/GenAi/data/quick-rag/data.txt")
        .split_documents()
        .embed_documents()
        .create_retriever()
        .load_llm()
        .build_qa_chain()
        .run_query("What is docker model runner?")
    )
    print("***"* 50 )
    print(response)
    print("==="* 50 )
