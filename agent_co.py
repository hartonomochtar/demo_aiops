from query_data import *
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
import pprint
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def agent_co(id):
    resp_co = query_data("co_db", id)
    
    log_output=""
    try:
        for data in resp_co["hits"]["hits"]:
            log_output = pprint.pformat(data["_source"]) + log_output
    except:
        log_output = "log not found"
    
    query_co = f"""You are an IT Support for CO system. You HAVE TO ANALYZE the log given.
    for your reference, below is/are data retrieve from log or database: 
    {log_output}
    """
    local_llm = Ollama(model="llama3.1:8b", request_timeout=600.0, base_url="ollama:11434")
    response = local_llm.complete(query_co)
    # llm = OpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    # response = llm.complete(query_co)
    return(response)
