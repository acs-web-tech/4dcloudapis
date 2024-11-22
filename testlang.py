from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient
from Readers.ExcelReader import ExcelReader
from Readers.WebReader import WebPageLoader
from langchain_community.vectorstores import Neo4jVector
import os
from FDStore.FDStore import FDVectorStore
import nest_asyncio
import asyncio
nest_asyncio.apply()



# CONNECTION_STRING = "mongodb+srv://avpalpandi:lakshmi%4087@cluster0.c8ufb3k.mongodb.net/"
# DB_NAME = "test"
# COLLECTION_NAME = "vector"
# INDEX_NAME = "vector_index"
# embeddings = OpenAIEmbeddings(model="text-embedding-3-large",dimensions=1024)
docs =ExcelReader("C:/Users/arun/Downloads/Online Sales Data.xls",
      mapping=["Transaction_ID","Date","Product_Category","Product_Name","Units_Sold","Unit_Price","Total_Revenue","Region","Payment_Method"],unique_id_gen=False,doc_id="Transaction_ID",make_embedding="Product_Name")
 
# db = Neo4jVector.from_documents(
#     [], OpenAIEmbeddings(), url="neo4j+s://e0998e63.databases.neo4j.io", username="neo4j", password="_Y1gdCskp2E8qQ076hNKI2F5w0-ihcMEE7Iuk5p6jgI",
# )
#relevant_documents = db.similarity_search

# for document in relevant_documents:
#     print("Document content:", document)
#     print()
# db._driver.close()
vectorStore =  FDVectorStore("neo4j://localhost:7687","neo4j","Lakshmi@87")
#docs = WebPageLoader(["https://python.langchain.com/v0.2/docs/integrations/document_loaders/web_base/","https://python.langchain.com/v0.2/docs/integrations/platforms/huggingface/"])
# print(vectorStore.FDStoreAdd())
# result  = vectorStore.FDStoreAdd(searchType="similarity_search_with_score",query="I need educational metairls",k=5)
# parser = map(lambda value:{"page_content":value[0].page_content},result)
vectorStore.createProject("acsind")