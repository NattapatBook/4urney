import mimetypes
import os
import shutil
from io import BytesIO
from urllib.parse import urlparse

import boto3
import nest_asyncio
import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document as LangChainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse
from openai import OpenAI
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)
# from sentence_transformers import SentenceTransformer, models
from tqdm.auto import tqdm
from apps.webhook_line.views import OPENAI_API_KEY

load_dotenv()

client = OpenAI(api_key=OPENAI_API_KEY)

def create_field_schema(schema, EMBEDDINGS_DIMENSION, TEXT_MAX_LENGTH):
    """Create field schemas for the collection."""
    final_schema = [FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True)]

    for key in schema:
        if schema[key] == DataType.FLOAT_VECTOR:
            curr_schema = FieldSchema(name=key, dtype=schema[key], dim=EMBEDDINGS_DIMENSION)
        elif schema[key] == DataType.VARCHAR:
            curr_schema = FieldSchema(name=key, dtype=schema[key], max_length=TEXT_MAX_LENGTH)
        elif schema[key] == DataType.FLOAT:
            curr_schema = FieldSchema(name=key, dtype=schema[key])
        elif schema[key] == DataType.DOUBLE:
            curr_schema = FieldSchema(name=key, dtype=schema[key])
        elif schema[key] == DataType.INT64:
            curr_schema = FieldSchema(name=key, dtype=schema[key])
        else:
            pass 
        final_schema.append(curr_schema)
    return final_schema

def create_collection_schema(fields, description="Fut Fit For Fun"):
    """Create a collection schema with the provided fields."""
    return CollectionSchema(fields=fields, description=description, enable_dynamic_field=True)

def initialize_collection(collection_name, schema, using='default'):
    """Initialize a collection with the given name and schema."""
    return Collection(name=collection_name, schema=schema, using=using)

def manage_collection(collection_name, schema, ID_MAX_LENGTH=50000, EMBEDDINGS_DIMENSION=1024, TEXT_MAX_LENGTH=50000):
    """Manage the creation or replacement of a collection."""
    print("Existing collections:", utility.list_collections())
    if collection_name in utility.list_collections():
        utility.drop_collection(collection_name)
        print("Dropped old collection")

    # Ensure collection is dropped
    existing_collections = utility.list_collections()
    print(f"Existing collections after drop operation: {existing_collections}")

    fields = create_field_schema(schema, EMBEDDINGS_DIMENSION, TEXT_MAX_LENGTH)
    print("Fields for new collection:", fields)

    schema = create_collection_schema(fields)
    collection = initialize_collection(collection_name, schema)
    print(f"Initialized new collection: {collection_name}")
    return collection

def initialize_db_client(MILVUS_COLLECTION_NAME, MILVUS_HOST='localhost', MILVUS_PORT=8000):
    """
    Initializes and returns a Milvusdb client.

    Parameters:
    - host (str): The host for the Milvusdb service. Default is 'localhost'.
    - port (int): The port for the Milvusdb service. Default is 8000.

    Returns:
    - Milvusdb.HttpClient: An initialized Milvusdb client.
    """
    try:
        return connections.connect(Collection=MILVUS_COLLECTION_NAME, host=MILVUS_HOST, port=MILVUS_PORT)
    except:
        return connections.connect(Collection=MILVUS_COLLECTION_NAME, host='host.docker.internal', port=MILVUS_PORT)
    

# def get_model(model_name='airesearch/wangchanberta-base-att-spm-uncased', max_seq_length=768, condition=True):
#     if condition:
#         word_embedding_model = models.Transformer(model_name, max_seq_length=max_seq_length)
#         pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),pooling_mode='cls') # We use a [CLS] token as representation
#         model = SentenceTransformer(modules=[word_embedding_model, pooling_model],cache_folder='./tmp')
#     return model

def get_retrival(model_embedder, question, collection, output_fields=['text_to_encode'], limit=3, ):
    if model_embedder is not None:     
        query_encode = list(model_embedder.encode([question]))
    else:
        query_encode = get_embeddings([[question]])
    collection.load()

    documents = collection.search(
                                data=query_encode, 
                                anns_field="embedding", 
                                param={"metric_type": "IP", "params": {}}, 
                                consistency_level="Strong",      
                                output_fields=output_fields, 
                                limit=limit)

    df_retrival = pd.DataFrame()
    for hit in documents[0]:
        _df = pd.DataFrame(hit.entity.__dict__).T.iloc[-1:,:]
        df_retrival = pd.concat([df_retrival, _df], axis=0)
    df_retrival.reset_index(drop=True, inplace=True)

    return df_retrival

def prepare_ingest_df(data_dictionary, model_embedder, focus_columns=True):
    
    data_dictionary.fillna('None', inplace=True)
    data_dictionary['id'] = [i for i in range(len(data_dictionary))]
    
    all_columns = data_dictionary.columns.to_list()

    encode_columns = {k:k for k in data_dictionary.columns}

    data_dictionary['text_to_encode'] = [
        ' '.join([f"{des}: {str(imf)}" for des,
                    imf in zip(encode_columns.values(), info)])
        for info in zip(*[data_dictionary[column] for column in encode_columns.keys()])
    ]
    
    embeds = []
    del_idx = []
    for index, text in tqdm(zip(data_dictionary.index, data_dictionary.text_to_encode)):
        try:
            # Attempt to encode the text
            if model_embedder is not None:
                embed = model_embedder.encode(text)
            else:
                embed = get_embeddings(text)
            # If successful, add it to your embeddings list
            embeds.append(np.array(embed).reshape(-1))
        except Exception as e:
            print(f"Error with text at index {index}: {text} as {e}")
            del_idx.append(index)

    # Select only embedded index. For the rest, got problem, ignore them.
    data_dictionary = data_dictionary.loc[~data_dictionary.index.isin(del_idx)]
    data_dictionary['embedding'] = embeds

    vals = {}
    all_columns.append('text_to_encode')
    for column in all_columns:
        vals[column] = data_dictionary[column].to_list()
    
    if focus_columns:
        return data_dictionary[['id', 'text_to_encode', 'embedding']]
    else:
        return data_dictionary


def data_ingestion_df(data,  collection_name):
    
    if collection_name in utility.list_collections():
        utility.drop_collection(collection_name)
        print("Dropped old collection")
        

    collection, ins_res = Collection.construct_from_dataframe(
        collection_name,
        data,
        primary_field='id',
        auto_id=False
        )

    index_params = {
        "metric_type": "IP",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 16384},
    }

    collection.create_index(field_name="embedding", index_params=index_params)

    # Flush the collection
    collection.flush()
    collection.load()
    print(f'Insert Data into {collection_name} had done')

def data_ingestion_pdf(data,  collection_name):
    
    if collection_name in utility.list_collections():
        utility.drop_collection(collection_name)
        print("Dropped old collection")
        

    collection, ins_res = Collection.construct_from_dataframe(
        collection_name,
        data,
        primary_field='id',
        auto_id=False
        )

    index_params = {
        "metric_type": "IP",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 16384},
    }

    collection.create_index(field_name="embedding", index_params=index_params)

    # Flush the collection
    collection.flush()
    print(f'Insert Data into {collection_name} had done')
    

# Function to get embeddings for multiple texts
def get_embeddings(docs_texts):
    # Get backend endpoint and port from environment variables
    be_endpoint = os.environ['BE_ENDPOINT']
    be_port = os.environ['BE_PORT']
    
    
    url = f"http://{be_endpoint}:{be_port}/embedded_data"
    
    # List to store the response data
    resp = []
    
    if type(docs_texts) is not list:
        docs_texts = [docs_texts]
    
    # Iterate over the documents and send the POST request
    for doc in tqdm(docs_texts):
        payload = {"text": doc}

        try:
            # Send the POST request to the backend
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                # Append the result to the response list
                resp.append(response.json()['embeddings'])  # You can store the embeddings here
            else:
                print(f"Error: {response.json()}")
        except Exception as e:
            print(f"Error during request for doc '{doc}': {str(e)}")

    return np.array(resp).squeeze(axis=1)


def read_pdf(pdf_path, chunk_size =1000, chunk_overlap=20, native_langchain=True):
    if native_langchain:
        loader = PyPDFLoader(pdf_path)

        #Load the PDF content
        documents = loader.load()
    
    else:
        nest_asyncio.apply()
        # set up parser
        parser = LlamaParse(
            result_type="markdown"  # "markdown" and "text" are available
        )

        # use SimpleDirectoryReader to parse our file
        file_extractor = {".pdf": parser}
        documents = SimpleDirectoryReader(input_files=[pdf_path], file_extractor=file_extractor).load_data()
        documents = [LangChainDocument(page_content=document.text, metadata=document.metadata) for document in documents]
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    
    return docs

def read_push_document(model_embedder, docs, collection_name):
    
    docs_texts = [doc.page_content for doc in docs]
    if model_embedder is not None:
        embeddings = []
        for docs in docs_texts:
            embedding = model_embedder.encode(docs)
            embeddings.append(embedding)
    else:
        embeddings = get_embeddings(docs_texts)
        
    embeddings = np.array(embeddings).astype("float32")
    doc_ids = np.array(range(len(docs_texts))).astype("int64")
    
    # Define the schema
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),  # Document IDs
        FieldSchema(name="text_to_encode", dtype=DataType.VARCHAR, max_length=4096),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=model_embedder.get_sentence_embedding_dimension()),  # Vector dimension
    ]
    schema = CollectionSchema(fields, description="Document embeddings collection")

    if collection_name in utility.list_collections():
        utility.drop_collection(collection_name)
        print("Dropped old collection")

    # Create the collection (if not exists)
    collection = Collection(name=collection_name, schema=schema)
    
    # Step 4: Insert data into the Milvus collection
    data = [doc_ids.tolist(), docs_texts, embeddings.tolist()]
    collection.insert(data)

    # Step 5: Create an index for fast search
    index_params = {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}}
    collection.create_index(field_name="embedding", index_params=index_params)
    collection.flush()
    collection.load()
    
    print(f"PDF ingested successfully into Milvus collection '{collection_name}'.")
    
def save_file_in_original_format(bucket_name, object_key, save_dir='./downloads/'):
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Get the file content
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    file_content = response['Body'].read()
    
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Determine the file extension from the key or MIME type
    file_extension = os.path.splitext(object_key)[-1]  # Extract extension from object key
    if not file_extension:
        mime_type, _ = mimetypes.guess_type(object_key)
        file_extension = mimetypes.guess_extension(mime_type) if mime_type else ''
    
    # Define the local save path
    file_name = os.path.basename(object_key)  # Extract file name from the key
    save_path = os.path.join(save_dir, file_name)
    
    # Save the file
    with open(save_path, 'wb') as file:
        file.write(file_content)
    print(f"File saved as {save_path}")

def extract_bucket_and_object(s3_url):
    # Parse the S3 URL
    parsed_url = urlparse(s3_url)
    
    # Extract bucket name and object key
    bucket_name = parsed_url.netloc.split('.')[0]  # Get the first part of the domain
    object_name = parsed_url.path.lstrip('/')  # Remove leading slash
    return bucket_name, object_name

def delete_save_dir(save_dir):
    """
    Deletes the specified directory and all its contents.

    Args:
        save_dir (str): The path to the directory to be deleted.

    Returns:
        bool: True if the directory was deleted successfully, False otherwise.
    """
    if os.path.exists(save_dir) and os.path.isdir(save_dir):
        try:
            shutil.rmtree(save_dir)
            print(f"Directory '{save_dir}' has been deleted successfully.")
            return True
        except Exception as e:
            print(f"An error occurred while deleting '{save_dir}': {e}")
            return False
    else:
        print(f"Directory '{save_dir}' does not exist.")
        return False
    
def get_file_details(object_name, save_dir):
    """
    Extracts organization name, file name, and constructs file path.

    Args:
        object_name (str): The full object path.
        save_dir (str): Directory where the file is saved.

    Returns:
        tuple: (organization name, file name, file path, collection name)
    """
    org_name = object_name.split('/')[0]
    file_name = object_name.split('/')[-1]
    file_path = os.path.join(save_dir, file_name)
    collection_name = f'org{org_name}__{file_name}'.replace('.', '_').replace(' ', '_')
    return org_name, file_name, file_path, collection_name


def process_excel(file_path):
    """
    Processes an Excel file by reading all sheets and preparing data.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        DataFrame: Combined data from all sheets.
    """
    excel_file = pd.ExcelFile(file_path)
    whole_df = pd.concat([
        prepare_ingest_df(
            pd.read_excel(file_path, sheet_name),
            model_embedder=ModelEmbedder(),
            focus_columns=True
        )
        for sheet_name in excel_file.sheet_names
    ], axis=0)
    return whole_df

def process_csv(file_path):
    """
    Processes a CSV file and prepares data for ingestion.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        DataFrame: Processed data.
    """
    df = pd.read_csv(file_path)
    ready_data = prepare_ingest_df(df, model_embedder=ModelEmbedder(), focus_columns=True)
    return ready_data

def process_pdf(file_path):
    """
    Processes a PDF file and extracts documents for ingestion.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        list: Processed documents.
    """
    docs = read_pdf(file_path, chunk_size=512, chunk_overlap=64, native_langchain=False)
    return docs

class ModelEmbedder:
    def get_embedding(self, text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return np.array(client.embeddings.create(input = [text], model=model).data[0].embedding)
    
    def get_sentence_embedding_dimension(self):
        return 1536

    def encode(self, text):
        return self.get_embedding(text)