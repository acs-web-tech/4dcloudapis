from transformers import BertTokenizerFast
from openai import OpenAI
import openai
import pymongo
import datetime
# connect to your Atlas cluster
BertTokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
class FDSVectorEmbeddings():
    def __init__(self) -> None:
        pass
    def embed_query(self,query):
        encode = BertTokenizer.tokenize(query)
       
emb = FDSVectorEmbeddings()
emb.embed_query("Hello world")