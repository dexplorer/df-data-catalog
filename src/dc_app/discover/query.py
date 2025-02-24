from langchain_text_splitters import (
    # Language,
    # RecursiveCharacterTextSplitter,
    # CharacterTextSplitter,
    RecursiveJsonSplitter,
)

from langchain.chains.retrieval import create_retrieval_chain#, RetrievalQA 
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import LanceDB

# from langchain_community.document_loaders import TextLoader

from config.settings import ConfigParms as sc
import os

from utils import json_io as ufj 

# openai_key = os.environ["OPENAI_API_KEY"]
openai_key = os.environ.get("OPENAI_API_KEY")


# def sql_doc_splitter(text_loader):
#     sql_splitter = RecursiveCharacterTextSplitter.from_language(
#         Language.SQL, chunk_size=3000, chunk_overlap=500
#     )
#     return text_loader.load_and_split(sql_splitter)


# def text_doc_splitter(text_loader):
#     text_splitter = CharacterTextSplitter(
#         separator="GO\n",
#         chunk_size=3000,
#         chunk_overlap=500,
#         length_function=len,
#         is_separator_regex=False,
#     )
#     return text_loader.load_and_split(text_splitter)


def json_doc_splitter(json_data):
    splitter = RecursiveJsonSplitter(max_chunk_size=300)
    # docs = splitter.create_documents(texts=[json_data])
    docs = splitter.create_documents(texts=json_data)
    return docs

def read_json_file(file_path: str):
    dicts = ufj.uf_read_json_file_to_list_of_dict(file_path=file_path)
    return dicts

def query_catalog():
    # text_loader = TextLoader("CEDS-Data-Warehouse-V11.0.0.0-truncated.sql")
    # text_loader = TextLoader("/workspaces/df-data-lineage-genai/dlgenai_app/data/ceds_dw.sql")
    json_file_path = f"{sc.data_out_file_path}/asset_dataset_3.json"
    json_data = read_json_file(file_path=json_file_path)
    print(json_data)
    docs = json_doc_splitter(json_data=json_data)
    print(docs)

    # Add to vectorDB
    vectorstore = LanceDB.from_documents(documents=docs, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()

    chat_model = ChatOpenAI(model="gpt-3.5-turbo")

    # RAG prompt
    prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    combine_docs_chain = create_stuff_documents_chain(chat_model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    question = """
    List all of the physical data elements that are classified as PII. 
    For each physical data element, list the system and business data element in the format:
    physical data element -> system data element -> business data element
    """

    answer = retrieval_chain.invoke({"input": question})

    print(answer["answer"])
