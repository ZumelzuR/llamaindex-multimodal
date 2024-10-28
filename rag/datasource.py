import os
from typing import List
from dotenv import load_dotenv
from llama_index.core.response.notebook_utils import display_source_node
from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import StorageContext

from utils.storage import create_meta_from_name
from utils.pdf import parse_pdf_folder

load_dotenv(override=True)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

from llama_index.core import SimpleDirectoryReader
from llama_index.core import load_index_from_storage


TAG = "RAG"
PDF_STORAGE_PATH = "data"
TEMP_IMAGE_PATH = os.path.join(PDF_STORAGE_PATH, "temp")

index_name_text = "text-index"
index_name_image = "images-index"

vector_store_info = VectorStoreInfo(
    content_info="Manuals",
    metadata_info=[
        MetadataInfo(
            name="item",
            description="Item of the ikea manual.",
            type="string",
        ),
        MetadataInfo(
            name="file_path",
            description="File path of the image of the manual",
            type="string",
        ),
    ],
)


def log(message):
    print(f" [{TAG}] {message}")


def init_pinecone(index_name_text=index_name_text, index_name_image=index_name_image):
    pc = Pinecone(api_key=PINECONE_API_KEY)
    pc_list = pc.list_indexes()
    if not any(index_name_text == idx["name"] for idx in pc_list.indexes):
        pc.create_index(
            name=index_name_text,
            dimension=1536,
            metric="dotproduct",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    if not any(index_name_image == idx["name"] for idx in pc_list.indexes):
        pc.create_index(
            name=index_name_image,
            dimension=512,
            metric="dotproduct",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    pinecone_index_text = pc.Index(index_name_text)
    pinecone_index_image = pc.Index(index_name_image)
    image_store = PineconeVectorStore(
        pinecone_index=pinecone_index_image, index_name=index_name_text
    )
    text_store = PineconeVectorStore(
        pinecone_index=pinecone_index_text, index_name=index_name_text
    )
    return text_store, image_store


def load_index(text_store, image_store):
    storage_context = StorageContext.from_defaults(
        vector_store=text_store, image_store=image_store, persist_dir="./storage"
    )
    index = load_index_from_storage(storage_context, image_store=image_store)
    return index


def ingest_data(text_store, image_store, image_temp_path=TEMP_IMAGE_PATH):
    log("Ingesting data...")
    parse_pdf_folder(PDF_STORAGE_PATH)
    documents = SimpleDirectoryReader(
        input_dir=image_temp_path,
        filename_as_id=True,
        recursive=True,
        file_metadata=create_meta_from_name,
    ).load_data()

    storage_context = StorageContext.from_defaults(
        vector_store=text_store, image_store=image_store
    )

    index = MultiModalVectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        store_nodes_override=True,
    )
    index.storage_context.persist(persist_dir="./storage")
    log("Ingestion done!")

    return index, storage_context


def init_datasource():
    text_store, image_store = init_pinecone()
    print("Pinecone initialized")
    index = load_index(text_store, image_store)
    return index
