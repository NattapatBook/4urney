import os
from langchain_openai import ChatOpenAI

def get_openai_model(max_tokens=1024):
    return ChatOpenAI(model_name="gpt-4o-mini", max_tokens=max_tokens)

def get_deepseek_v3_model(max_tokens=1024): 
    return ChatOpenAI(model_name="deepseek/deepseek-chat:free", max_tokens=max_tokens)