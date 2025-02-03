from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain

def get_multi_routing_chain(chat_history, routing, retrieval_text, df, model):
    """
    Multi-routing RAG chain
    """

    rag_text = f"""
    # Current conversation: 
        {chat_history}
        
    # Your knowledge: 
        {retrieval_text}
    """

    qa_text = """
    Question: {input}
    Answer: 
    """

    template = str(df[df.routing == routing]['prompt'].values[0]) + '\n' + str(rag_text) + '\n' + str(qa_text)

    prompt_template = PromptTemplate(template=template, input_variables=['input'])

    prompt_and_model = prompt_template | model

    return prompt_and_model