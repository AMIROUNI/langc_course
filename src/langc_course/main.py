
from dotenv import load_dotenv
from importlib.metadata import version

from clients.ollama_client import OllamaCloudClient

load_dotenv() # load environment variables from .env file



print(f"langchain-core version: {version('langchain-core')}")
print(f"langgraph version: {version('langgraph')}")



def main():

    llm = OllamaCloudClient(
        embedding_model="embeddinggemma",
        model="gemma4:31b",
        temperature=0
    )

    response = llm.invoke(
        "Explain LangChain in simple terms."
    )


    print(response)


if __name__ == "__main__":
    main()




