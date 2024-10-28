from rag import datasource
from rag.datasource import init_pinecone


def ingest_data_task():
    print("init task")
    text_store, image_store = init_pinecone()
    datasource.ingest_data(text_store, image_store)
    print("end task")
