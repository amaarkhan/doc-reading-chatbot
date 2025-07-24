from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def load_and_split_document(file_path):
    loader = TextLoader(file_path)
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents(docs)
