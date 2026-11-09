"""
LangSmith Setup and Observability 
Production monitoring for LangChain/LangGraph

"""


import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith import traceable
from langsmith.run_trees import RunTree
from langc_course.clients.ollama_client import OllamaCloudClient
from langc_course.vector_db_using_chroma.ollama_embedding_adapter import OllamaEmbeddingAdapter
from dotenv import load_dotenv


load_dotenv()




#Enable tracing 
os.environ["LANGSMITH_TRACING"]="true"



@traceable
def demo_basic_tracing():
    """Basic LangSmith tracing"""

    llm=OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0
)

    prompt= ChatPromptTemplate.from_template(
        "Explain {topic} in one sentence."
    )

    chain = prompt |llm| StrOutputParser()


    print("Basic Tracing Demo: \n") 
    print("Running chain with LangSmith tracing enabled ...")

    result= chain.invoke({"topic: machine learning"})

    print(f"Result: {result}")

    print("\n Check LangSmith dashboard for trace details")



@traceable(name="named_runs_demo",tags=["production","summarization"])
def demo_name_runs():
    llm=OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0
)

    prompt= ChatPromptTemplate.from_template(
        "Explain {topic} in one sentence."
    )

    chain = prompt |llm| StrOutputParser()


    print(" Tracing Demo with name : \n") 
    print("Running chain with LangSmith tracing enabled ...")

    result= chain.invoke({"topic: deeplearning"})

    print(f"Result: {result}")

    print("\n Check LangSmith dashboard for trace details")




@traceable(name="trace_with_metadata_demo",tags=["metadata","filtering"])
def demo_traca_with_metadata(user_id:str,request_type:str):
    """Add metatdata to traces for filtering"""
    llm= OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0
)
    # Metadata is automaticaly captured

    result= llm.invoke(f"Hello from user {user_id}")
    return result.content

if __name__=="__main__":
    demo_basic_tracing()
    demo_name_runs()
    demo_traca_with_metadata(user_id="user_1234545",request_type="greeting")


