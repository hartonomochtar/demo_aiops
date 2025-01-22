from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def agent_reviewer(user_input, answer):
    query_review = f"""Your main task is to double check and review the given statement from AI Agent is correlate with the Original Question from user. 
    You will have 2 inputs, which is original question from user, and response from AI agent.
    Output: A JSON object (without prefix '```json' and suffix '```'  with the following keys:
        'score' (int): 0-100 0 is the lowest and 100 is the highest
        'reason' (str): give your brief and clear reason and explanation

    ## Original Question:
    {user_input}

    ## AI Agent Response:
    {answer}
    """
    local_llm = Ollama(model="llama3.1:8b", request_timeout=600.0, base_url="ollama:11434")
    response = local_llm.complete(query_review)
    # llm = OpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    # response = llm.complete(query_review)

    print("Agent Review Query")
    print(query_review)
    print("Agent Review Response")
    print(response)
    return(response)
