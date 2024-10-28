import os
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv

from llama_index.multi_modal_llms.openai import OpenAIMultiModal

load_dotenv(override=True)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


class StandarOpenAIBuilder:
    """
    A builder class for initializing and configuring OpenAI models for multimodal tasks.

    This class is designed to facilitate the implementation of different kinds of models
    (e.g., Azure, other providers) by centralizing the configuration and initialization
    logic in one place.

    Attributes:
        llm (OpenAIMultiModal): The language model initialized with the specified parameters.
        embed_model (OpenAIEmbedding): The embedding model initialized with the specified parameters.
        num_output (int): The number of output tokens.
        context_window (int): The context window size for the model.

    Args:
        model (str): The name of the language model to use. Default is "gpt-4o".
        temperature (float): The temperature setting for the language model. Default is 0.01.
        embedding_engine (str): The name of the embedding engine to use. Default is "text-embedding-3-small".

    Methods:
        get_config():
            Returns the configuration of the initialized models and settings.
    """

    def __init__(
        self,
        model="gpt-4o",
        temperature=0.01,
        embedding_engine="text-embedding-3-small",
    ):
        self.llm = OpenAIMultiModal(
            model=model, api_key=OPENAI_API_KEY, temperature=temperature
        )

        self.embed_model = OpenAIEmbedding(
            model=embedding_engine,
        )

        self.num_output = 512
        self.context_window = 3900

    def get_config(self):
        return {
            "llm": self.llm,
            "embed_model": self.embed_model,
            "num_output": self.num_output,
            "context_window": self.context_window,
        }
