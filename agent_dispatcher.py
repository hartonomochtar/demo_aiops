from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from agent_trace import *
from agent_esb import *
from agent_co import *
from agent_ufo import *
from agent_c2p import *
from agent_reviewer import *
from agent_greeter import *
from query_data import *
import json
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def agent_dispatcher(user_input):
    print(user_input)
    query_1 = f"""You are an AI Agent tasked to identify and discern specific values within a user input. You also specialize in linguistics and understanding the intent of user questions.
    
    Do NOT mention any of these instructions in the final answer.
    You must know the following background information regarding values you may encounter in the user input. If any values you encounter fit the given criteria below, you must immediately recognize the following types of values regardless of the word preceding or following it:
    1. Order ID or Transaction ID: Alphanumeric value with 25-26 characters.
    	An 'Order' might be referred to as a 'Transaction', these two terms are used interchangeably.
    2. Serial Number: Numeric value, 12 digits.
    	Usually starts with digit 1. May also be referred to as an ID or IH Number.
    3. PSTN or Phone Number: Numeric value, 10 to 12 digits.
    	Usually starts with digit 0.
    4. Available systems consist of the following: ESB, CO, UFO, C2P
    
    You must analyze the intent of this user question/input. Identify whether the user is asking about an order/orders.
    
    The question may also be asked in Bahasa Indonesia or Indonesian language.
    In this case, translate the question first to English before making the decision. 
    
    Strictly focus on this task only, do not hallucinate and be polite.
    
    YOUR JOB is to output a JSON object without prefix 'json' and suffix '' with the following keys:
    'query': the original query without any modifications.
    'category' (str): A string that defines the query. Possible values:
            'greeting': if the query is related to greeting or compliment or praise or non-order/system related.
            'check order': if the query explicitly mentions check order or if the user question is related to orders. If you find "check order" in the query immediately recognize it as as check order question.
    'system' (str): A string that defines the system that the user wants to search from. Possible values:
            'ESB' if the query mentions ESB system
            'CO': if the query mentions CO system
            'UFO': if the query mentions UFO system
            'C2P': if the query mentions C2P system
            'ALL': if the query does not mention any system
    'serialnumber' (str): A Serial Number provided in the question. If you find a 12 digit number starting with 1 in {user_input}, immediately insert it here.
    'PSTN' (str): A string of PSTN or phone number provided in the question.
    'orderID' (str): An Order ID or Transaction ID provided in the question, must be alphanumeric and 25-26 characters.

    ## ORIGINAL QUERY
    {user_input}
    
    """
    local_llm = Ollama(model="llama3.1:8b", request_timeout=600.0, base_url="ollama:11434")
    response = local_llm.complete(query_1)
    
    # llm = OpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    # response = llm.complete(query_1)
    print(response)

    try:
        response_json = None
        if response.text:
            response_json = json.loads(response.text)

        if response_json['category'] == 'N/A':
            resp = "Sorry I'm unable to help with your question."
            print ("Sorry I'm unable to help with your question.")
        elif response_json['category'] == 'greeting':
            resp = agent_greeter(user_input)
        elif response_json['category'] == 'check order':
            if response_json['system'] == 'ALL':
                resp = agent_trace(response_json['serialnumber'])
            elif response_json['system'] == 'ESB':
                resp = agent_esb(response_json['serialnumber'])
            elif response_json['system'] == 'CO':
                resp = agent_co(response_json['serialnumber'])
            elif response_json['system'] == 'CO':
                resp = agent_ufo(response_json['serialnumber'])
            elif response_json['system'] == 'C2P':
                resp = agent_c2p(response_json['serialnumber'])

            resp_review_json = None
            resp_reviewer = agent_reviewer(user_input,resp)
            resp_reviewer_json = json.loads(resp_reviewer.text)

            print(resp_reviewer)
            
            if resp_reviewer_json['score'] >= 70:
                print(resp)
            else:
                resp = "Sorry, I'm unable to answer your query" 
                print("Sorry, I'm unable to answer your query")

    except:
        resp = "Sorry there is something wrong with me. Please contact administrator."
        print("Sorry there is something wrong with me. Please contact administrator.")
    
    return(resp)
