from llama_index.core.tools import FunctionTool
from pydantic import Field
import os
from engine import StandarOpenAIBuilder
from rag.datasource import init_datasource, vector_store_info
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)
from llama_index.core.schema import ImageNode
from llama_index.core.schema import ImageDocument

build = StandarOpenAIBuilder()
index = init_datasource()


def retriever_custom(
    query: str = Field(
        description="Original query from the user, should be always the original one",
        examples=["Which ones are the tools of the tuffle furniture?"],
    ),
    filter_entinty: str = Field(
        description="The primary entity the user is inquiring about, typically the item for which they need instructions from the manual. Must be in lowercase and just one word",
        examples=["tuffle"],
    ),
):
    retriever_engine = index.as_retriever(
        similarity_top_k=3,
        image_similarity_top_k=10,
        vector_store_info=vector_store_info,
        verbose=True,
        filters=MetadataFilters(
            filters=[
                MetadataFilter(
                    key="item",
                    operator=FilterOperator.EQ,
                    value=filter_entinty,
                ),
            ]
        ),
    )

    retrieval_results = retriever_engine.text_to_image_retrieve(query)
    retrieved_images = []
    for res_node in retrieval_results:
        if isinstance(res_node.node, ImageNode):
            retrieved_images.append(res_node.node.metadata["file_path"])

    image_documents = [
        ImageDocument(image_path=image_path) for image_path in retrieved_images
    ]
    response = build.llm.complete(
        prompt=query,
        image_documents=image_documents,
    )
    return response


def get_product_list():
    with os.scandir("data") as entries:
        products = [entry.name for entry in entries if entry.is_file()]
    return ", ".join(products)


def setup_tools():
    image_retriever_tool = FunctionTool.from_defaults(
        fn=retriever_custom,
        description="Agent that will interpretate ikea manuals, so will be usefull for answer question related to that. You must pass the query and the main entity to the function tool. You must go and call the function always to get the images from the documents. If you not have results, maybe call first get_product_list_tool",
    )
    get_product_list_tool = FunctionTool.from_defaults(
        fn=get_product_list,
        description="Tool that provide list of products and names in the storage, usefull when user mistake with the name or you can't find the product",
    )
    return [image_retriever_tool, get_product_list_tool]
