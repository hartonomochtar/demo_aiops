from query_data import *
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def agent_trace(id):
    data_esb = query_data("esb-db", id)
    data_ufo = query_data("ufo-db", id)
    data_co = query_data("co_db", id)
    data_c2p = query_data("c2p-db", id)

    if data_esb == "":
        data_esb = "No available logs."

    if data_ufo == "":
        data_ufo = "No available logs."

    if data_co == "":
        data_co = "No available logs."

    if data_c2p == "":
        data_c2p = "No available logs."

    query_trace = f"""
        You are an expert in system troubleshooting to find the root causes of the issues.
        The information related to order details, list of systems, workflow diagram, workflow description and detailed system logs are given below.
        
        Use all the available context, information and facts and perform your holistic analysis.

        When there are multiple systems or services having issues in your analysis, always prioritize the southbound or downstream service or system as the top root cause.

        
            Imagine there are 4 different experts in system troubleshooting.
            For each iteration, each experts will write down 1 step of their thinking, then share it within the group.
            Then all experts will go to the next iteration.
        

        Do not hallucinate and do not use any other information or actions other than given facts.

        The response is returned as a JSON object with the following keys, but do not put json prefix in front of it.
        For the analysis, give in  markdown point and newline format, do not apply bold. highlight the service or system name in markdown code style.

        Returns dict: A JSON object (do not put json prefix in front of it) containing the following keys:
            'score' (int): 0-100 0 is the lowest and 100 is the highest
            'rca' : give the main root cause based on your analysis.
            'analysis': give your brief and clear root cause analysis in markdown point and newline format. you MUST include the number or id given into the root cause analysis. 
                        if you found any error from log, you MUST provide the error message and explain briefly for the error.
    
        ## ISSUE
        Order process analysis

        ## IDENTIFIER
        {id}
    
        ## LIST OF SYSTEM
        1. esb : middleware between channel and order system
        2. co : order system to register and process the order request
        3. ufo : fulfillment system and integrate with surrounding third party system
        4. c2p : system of record for product and/or service belong to the customer
    

        ## WORKFLOW DIAGRAM

        sequenceDiagram
            participant esb as fmcordersubmission-bs
            participant co as co-bs
            participant ufo as ufo-bs
            participant c2p as c2p-bs
            
            esb->>co: Submit order to CO system
            co->>ufo: Process order to UFO system for fulfillment system
            ufo->>c2p: Once fulfillment complete, register product and/or service to C2P system
            
        ## WORKFLOW DESCRIPTION
        1. fmcordersubmission-bs → co-bs
        The first step involves the service esb-bs calls co-bs service to submit the order request from channel.
        esb-bs is passing some data or request to co-bs, for validation, retrieval, or processing.
        
        2. co-bs → ufo-bs
        After co-bs processes the order request data or performs its task, it then calls ufo-bs service for the fulfillment process.
        ufo-bs will then orchestrate the fulfillment process and integrate with third-party system to fulfill the order request.
        
        3. ufo-bs → c2p-bs
        Finally, once the process completed in ufo, ufo-bs calls c2p-bs service to register the product and/or service under the customer.
            
        ## SYSTEM LOGS
        ### 1. fmcordersubmission-bs    
        {data_esb}
        
        ### 2. co-bs
        {data_co}
        

        ### 3. ufo-bs
        {data_ufo}


        ### 4. c2p-bs
        {data_c2p}
        
    """
    # local_llm = Ollama(model="mistral", request_timeout=600.0)
    # response = local_llm.stream_complete(query_trace)
    
    llm = OpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    response = llm.complete(query_trace)

    response_json = None
    response_json = json.loads(response.text)
    return(response_json['analysis'])