from langchain.prompts.prompt import PromptTemplate

def get_multi_routing_chain(chat_history, routing, retrieval_text, df, model):
    """
    Multi-routing RAG chain
    """

    rag_text = f"""
    # Chat history: 
        {chat_history}
        
    # Your knowledge: 
        {retrieval_text}
    """

    qa_text = """
    Question: {input}
    Answer: 
    """
    if routing == "":
        template = str(rag_text) + '\n' + str(qa_text)
    else: 
        template = str(df[df.routing == routing]['prompt'].values[0]) + '\n' + str(rag_text) + '\n' + str(qa_text)

    prompt_template = PromptTemplate(template=template, input_variables=['input'])

    prompt_and_model = prompt_template | model

    return prompt_and_model