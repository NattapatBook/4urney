import os
import pandas as pd
from langsmith.anonymizer import create_anonymizer

from apps.bot.rag_utils import hugging_face_embeddings, get_milvus_retriever
from apps.bot.routing_utils import intent_routing_using_huggingface #  for further development
from apps.bot.model_utils import get_openai_model
from apps.bot.chain_utils import get_multi_routing_chain

def call_bot(chat_history: str, routing: str, message: str, retrieval_text: str, df_routing_config: pd.DataFrame):
    
    # routing = "พูดคุยหรือสอบถามทั่วไป"
    
    prompt_template = get_multi_routing_chain(chat_history=chat_history, routing=routing, retrieval_text=retrieval_text, df=df_routing_config, model=get_openai_model())
    
    reply_message = prompt_template.invoke({"input": message})
    
    return reply_message


def set_anonymizer(): 
    # create anonymizer from list of regex patterns and replacement values
    anonymizer = create_anonymizer([
        { "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}", "replace": "<email-address>" },
        { "pattern": r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", "replace": "<UUID>" }
    ])
    return anonymizer