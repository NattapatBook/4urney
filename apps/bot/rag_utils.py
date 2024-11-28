from langchain_huggingface import HuggingFaceEmbeddings
from langchain_milvus.vectorstores import Milvus

def hugging_face_embeddings(hf_model="intfloat/multilingual-e5-base"):
    """
    Create customer embeddings using huggingface
    """
    embeddings = HuggingFaceEmbeddings(
            # huggingfacehub_api_token=api_key, 
            model_name=hf_model
        )
    
    return embeddings

def get_milvus_retriever(uri, embeddings, collection_name="HR_4Plus"):
    """
    Get retriever from the following vector db (Milvus)
    """

    # The vectorstore to use to index the summaries
    vectorstore = Milvus(
        embeddings,
        connection_args={"uri": uri},
        collection_name=collection_name,
    )

    return vectorstore