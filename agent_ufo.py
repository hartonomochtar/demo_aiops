from query_data import *
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
import pprint
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def agent_ufo(id):
    resp_ufo = query_data("ufo-db", id)
    log_output=""
    try:
        for data in resp_ufo["hits"]["hits"]:
            log_output = pprint.pformat(data["_source"]) + log_output
    except:
        log_output = "log not found"
    
    query_ufo = f"""You are an IT Support for CO system. You HAVE TO ANALYZE the log given.
    for your reference, below is/are data retrieve from log or database: 
    {log_output}
    """
    # local_llm = Ollama(model="mistral", request_timeout=600.0)
    # response = local_llm.stream_complete(query_ufo)
    
    llm = OpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    response = llm.complete(query_ufo)
    return(response.text)