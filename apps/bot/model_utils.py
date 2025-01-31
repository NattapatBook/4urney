import os
from openai import OpenAI
from langchain_openai import ChatOpenAI

def get_openai_model(max_tokens=1024):
    return ChatOpenAI(model_name="gpt-4o", max_tokens=max_tokens)

def get_native_openai_model():
    return OpenAI()