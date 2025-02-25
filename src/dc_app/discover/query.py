from langchain import hub
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveJsonSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model

from utils import json_io as ufj

import getpass
import os
from typing import Any


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define state for application
class LLMApp:
    llm: Any
    embeddings: Any
    vector_store: Any
    prompt: Any

    def __init__(self, chat_model: str, model_provider: str, embedding_model: str):
        if not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

        self.llm = init_chat_model(model=chat_model, model_provider=model_provider)
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = InMemoryVectorStore(self.embeddings)
        # Define prompt for question-answering
        self.prompt = hub.pull("rlm/rag-prompt")

    # Define application steps
    def retrieve(self, state: State):
        retrieved_docs = self.vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}

    def generate(self, state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = self.prompt.invoke(
            {"question": state["question"], "context": docs_content}
        )
        response = self.llm.invoke(messages)
        return {"answer": response.content}

    def build_graph(self):
        # Compile application and test
        graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        graph = graph_builder.compile()
        return graph


def query_catalog(all_assets_data_file_path: str):
    app = LLMApp(
        chat_model="gpt-4o-mini",
        model_provider="openai",
        embedding_model="text-embedding-3-small",
    )

    # Get and split docs into chunks
    json_data = read_json_file(file_path=all_assets_data_file_path)
    doc_splits = json_doc_splitter(json_data=json_data)
    print(f"doc splits: {len(doc_splits)}")
    # print(doc_splits[:2])

    # Index chunks
    _ = app.vector_store.add_documents(documents=doc_splits)

    # Build app graph
    graph = app.build_graph()

    # response = graph.invoke(
    #     {
    #         "question": "List all of the physical data elements that are classified as PII."
    #     }
    # )
    # print(response["answer"])

    response = graph.invoke(
        {
            "question": """
            List the data elements needed to get the asset value for customers residing in the state of CA. 
            For each data element, list the physical data element names in the format:
            asset name -> physical data element name
            Examples:
            Customer -> state
            """
        }
    )
    print(response["answer"])


def read_json_file(file_path: str):
    dicts = ufj.uf_read_json_file_to_list_of_dict(file_path=file_path)
    return dicts


def json_doc_splitter(json_data):
    splitter = RecursiveJsonSplitter(max_chunk_size=3000)
    # docs = splitter.create_documents(texts=[json_data])
    docs = splitter.create_documents(texts=json_data)
    return docs
