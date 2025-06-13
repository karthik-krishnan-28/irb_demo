import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def load_local_texts(corpus_dir="corpus"):
    documents = []
    metadata = []

    for fname in os.listdir(corpus_dir):
        if not fname.endswith(".txt"):
            continue
        with open(os.path.join(corpus_dir, fname), "r") as f:
            content = f.read()
            documents.append(content)
            metadata.append({"source": fname})

    return documents, metadata

def build_vector_store(model_name="BAAI/bge-small-en-v1.5", chunk_size=512):
    docs, metas = load_local_texts()

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=50)
    chunks = []
    chunk_meta = []

    for doc, meta in zip(docs, metas):
        for chunk in splitter.split_text(doc):
            chunks.append(chunk)
            chunk_meta.append(meta)

    embed_model = HuggingFaceEmbeddings(model_name=model_name)
    vector_store = FAISS.from_texts(chunks, embed_model, metadatas=chunk_meta)

    return vector_store, embed_model
