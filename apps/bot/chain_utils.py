from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

def get_multi_routing_chain(routing, retrieval_text, df, model):
    """
    Multi-routing RAG chain
    """

    memory=ConversationBufferWindowMemory(k=5)

    rag_text = f"""
    # Your knowledge: 
        {retrieval_text}
    """

    qa_text = """
    # Current conversation: 
        {history}

        {input}
    """

    template = str(df[df.routing == routing]['prompt'].values[0]) + '\n' + str(rag_text) + '\n' + str(qa_text)

    print(template)

    prompt = PromptTemplate(input_variables=['history', 'input'], template=template)

    conversation = ConversationChain(
        llm=model,
        prompt=prompt,
        verbose=False,
        memory=memory
    )

    return conversation