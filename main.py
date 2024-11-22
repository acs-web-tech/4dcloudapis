from llama_index.core.settings import Settings

from llama_index.llms.openai import OpenAI
from Readers.ExcelReader import ExcelReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from FDStore.FDStore import FDVectorStore
from llama_index.core.schema import IndexNode
vector_store = FDVectorStore("neo4j://localhost:7687","neo4j","Lakshmi@87")

embed_model=OpenAIEmbedding(model="text-embedding-3-small",dimensions=256)


llm=OpenAI(api_key="sk-proj-qoqpQjFxWEw2XXYDmHDTT3BlbkFJ7ummpGMneSY3yxj8L00O")

Settings.llm=llm

Settings.embed_model=embed_model
storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)
docs =ExcelReader("C:/Users/arun/Downloads/Online Sales Data.xls",
      mapping=["Transaction_ID","Date","Product_Category","Product_Name","Units_Sold","Unit_Price","Total_Revenue","Region","Payment_Method"],unique_id_gen=False,doc_id="Transaction_ID",make_embedding="Product_Name")
 
index = VectorStoreIndex.from_documents(
    docs, storage_context=storage_context
)
query_engine = index.as_query_engine
obj = IndexNode(
    text="A query engine describing X, Y, and Z.",
    obj=query_engine,
    index_id="my_query_engine",
)

index = VectorStoreIndex(nodes=nodes, objects=[obj])
retriever = index.as_retreiver(verbose=True)