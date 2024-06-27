from flask import Flask,request
import json
import sys
from langchain_core.output_parsers import JsonOutputParser
from controllers.validateapi import validateApi, filevalidate
from controllers.storefiles import storageUtils,json_to_doc,vector_search,vector_node_list,vector_delete
from pymongo import MongoClient
from io import BytesIO
sys.path.insert(0,"/Users/arun/Documents/GitHub/4dcloudapis/")
from FDStore.FDStore import FDVectorStore
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/datasetupload"
Mongoconnection = MongoClient("mongodb://localhost:27017/")
@app.route('/insertvector',methods=["post"])
def insert_vector_by_file():
   if validateApi(request,Mongoconnection) and filevalidate(request) :
      if storageUtils(request,projectid=request.form.get("projectid")) : 
          return {"status":200,"upserted":True}
   return {"status":400,"upserted":False}

@app.route("/apis/insertvector_json",methods=["post"])
def insert_by_json():
   if validateApi(request,Mongoconnection):
      if json_to_doc(request):
         return {"status":200,"upserted":True}
   else :
      return {"status":200,"matches":"User not authorized"} 
   return {"status":400,"upserted":False}

@app.route("/apis/search_vector",methods=["post"])
def search_vector():
    if validateApi(request,Mongoconnection):
      result = vector_search(request) 
      if len(result)>0:
         return result 
    else :
          return {"status":200,"matches":"User not authorized"} 
    
@app.route("/apis/list_node",methods=['post'])
def list_node():
    if validateApi(request,Mongoconnection):
       result = vector_node_list(request)
       return result
    else :
        return {"status":200,"matches":"User not authorized"}
@app.route("/apis/delete_node",methods=["post"])
def delete_by_select():
   if validateApi(request,Mongoconnection):
      try :
          result  = vector_delete(request)
          return {"status":200,"message":"Deleted"}
      except :
          return {"status":200,"message":"Delete Failed!"}
   else :
      return {"status":200,"matches":"User not authorized"}


if __name__ == '__main__':
   app.run(debug=False)