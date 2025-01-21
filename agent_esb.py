from query_data import *
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def agent_esb(id):
    resp_esb = query_data("index_esb", id)
    query_esb = f"""You are an IT Support for CO system. you analyze and provide details based on data retrieve from database as below: 
    {resp_esb}
    """
    # local_llm = Ollama(model="mistral", request_timeout=600.0)
    # response = local_llm.stream_complete(query_esb)

    llm = OpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    response = llm.complete(query_esb)
    return(response)