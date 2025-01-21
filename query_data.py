from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()
elastic_user = os.getenv("ELASTIC_USER")
elastic_password = os.getenv("ELASTIC_PASSWORD")
elastic_cloud_id = os.getenv("ELASTIC_CLOUD_ID")


def query_data(index,query_str):
    client = Elasticsearch(cloud_id=elastic_cloud_id, basic_auth=(elastic_user, elastic_password))
    # ELASTIC_PASSWORD = "NtfSjFFMcmOJ48*8xjQ-"
    # client = Elasticsearch('http://localhost:9200', basic_auth=("elastic", ELASTIC_PASSWORD))
    resp_data = client.search(index=index, query={"multi_match": {"query": query_str}})
    return(resp_data)