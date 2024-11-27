import os
from langchain_community.chat_models import ChatOpenAI

def get_openai_model(max_tokens=1024):
    return ChatOpenAI(model_name="gpt-4o", max_tokens=max_tokens)