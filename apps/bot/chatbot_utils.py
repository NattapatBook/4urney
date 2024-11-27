import os
import pandas as pd

from apps.bot.rag_utils import hugging_face_embeddings, get_milvus_retriever
from apps.bot.routing_utils import intent_routing_using_huggingface #  for further development
from apps.bot.model_utils import get_openai_model
from apps.bot.chain_utils import get_multi_routing_chain

def call_bot(message: str, df_routing_config: pd.DataFrame, HUGGINGFACEHUB_API_KEY: str, MILVUS_URI: str, MILVUS_COLLECTION_NAME_DRONE: str):
    
    embeddings = hugging_face_embeddings(HUGGINGFACEHUB_API_KEY)
    vectorstore = get_milvus_retriever(uri=MILVUS_URI, embeddings=embeddings, collection_name=MILVUS_COLLECTION_NAME_DRONE)
    
    docs = vectorstore.similarity_search(message, k=2)
    contents = [doc.page_content for doc in docs]
    retrieval_text = '\n'.join(contents)
    
    routing = "พูดคุยหรือสอบถามทั่วไป"
    
    conversation = get_multi_routing_chain(routing=routing, retrieval_text=retrieval_text, df=df_routing_config, model=get_openai_model())
    
    reply_message = conversation.predict(input=message)
    
    return reply_message