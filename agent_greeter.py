from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def agent_greeter(user_input):
    query = f"""
    Your main task is to respond to any greeting or compliment or praise in a brief, positive and polite manner from the original query.
    if the original query doesn't related with checking order or transaction, reply politely that you are designed to help with order checking, 
    and offer help to check.

    ## Original Query
    {user_input}
    
    """
    # local_llm = Ollama(model="mistral", request_timeout=600.0)
    # response = local_llm.stream_complete(query_ufo)
    
    llm = OpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    response = llm.complete(query)
    return(response.text)