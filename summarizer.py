from langchain.chains.summarize import load_summarize_chain
from utils import llm, CustomDocumentLoader

def summarize():
    loader = CustomDocumentLoader("content.txt")
    doc = loader.load()
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.run(doc)

