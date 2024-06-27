from flask import Flask,request
import json
import sys
from langchain_core.output_parsers import JsonOutputParser
from controllers.validateapi import validateApi, filevalidate
from controllers.storefiles import storageUtils,json_to_doc,vector_search
from pymongo import MongoClient
from io import BytesIO
sys.path.insert(0,"/Users/arun/Documents/GitHub/4dcloudapis/")
from FDStore.FDStore import FDVectorStore
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/datasetupload"
Mongoconnection = MongoClient("mongodb://localhost:27017/")
@app.route('/insertvector',methods=["post"])
def insert_vector_by_file():
   print(request.get_data(parse_form_data=True),request.get_json())
   print(validateApi(request,Mongoconnection) ,filevalidate(request) )
   if validateApi(request,Mongoconnection) and filevalidate(request) :
      if storageUtils(request,projectid=request.form.get("projectid")) : 
          return {"status":200,"upserted":True}
   return {"status":400,"upserted":False}
@app.route("/insertvector_json",methods=["post"])
def insert_by_json():
   if validateApi(request,Mongoconnection):
      if json_to_doc(request):
         return {"status":200,"upserted":True}
   return {"status":400,"upserted":False}
@app.route("/search_vector",methods=["post"])
def search_vector():
    if validateApi(request,Mongoconnection):
      result = vector_search(request) 
      if len(result)>0:
         return result
      else :
         return {"status":200,"matches":"No match found"}
       

if __name__ == '__main__':
   app.run(debug=False)