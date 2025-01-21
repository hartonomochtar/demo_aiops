from query_data import *
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def agent_c2p(id):
    resp_c2p = query_data("index_c2p", id)
    query_c2p = f"""You are an IT Support for C2P system. you analyze and provide details based on data retrieve from database as below: 
    {resp_c2p}
    """
    # local_llm = Ollama(model="mistral", request_timeout=600.0)
    # response = local_llm.stream_complete(query_c2p)

    llm = OpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    response = llm.complete(query_c2p)
    return(response)