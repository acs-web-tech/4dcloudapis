from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import nest_asyncio
nest_asyncio.apply()
load_dotenv()
class FDVectorStore :
    def __init__(self,url,username,password) -> None:
        self.dbconnection = Neo4jVector(embedding=OpenAIEmbeddings(dimensions=1536,model="text-embedding-3-large"),url=url,username=username, password=password)
        self.connectionString =url
        self.username =  username
        self.password = password
        self.queryStore = None
      
    def FDStoreAdd(self,embedding=None,docs=[]):
        if self.dbconnection == None:
           try :
             self.dbconnection = Neo4jVector.from_documents(documents=docs)
             if  self.dbconnection :     
               return "Upserted"
           except Exception as error:
               print(error)
               return None 
    def QueryMethodSetter(self,methodName=""):
       self.queryStore = {
          "similarity_search_with_score":self.dbconnection.similarity_search_with_score,
          "asimilarity_search_by_vector":self.dbconnection.asimilarity_search_by_vector,
          "asimilarity_search":self.dbconnection.asimilarity_search,
          "amax_marginal_relevance_search":self.dbconnection.amax_marginal_relevance_search,
          "amax_marginal_relevance_search_by_vector":self.dbconnection.amax_marginal_relevance_search_by_vector,
          "asimilarity_search_with_relevance_scores":self.dbconnection.asimilarity_search_with_relevance_scores,
          "max_marginal_relevance_search":self.dbconnection.max_marginal_relevance_search
       }          
    def FDStorequery(self,**kargs):
       #searchType=str,query=str,n=int,embedding=[],lambda_mult=0.5
       #query,k=n,embedding=embedding,lambda_mult=lambda_mult
       self.QueryMethodSetter(kargs["searchType"])
       doc = self.queryStore[kargs["searchType"]](**kargs)
       return doc
    def close(self):
       return self.dbconnection._driver.close()
    