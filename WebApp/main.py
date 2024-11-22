from flask import Flask,request,jsonify
from flask_cors import CORS,cross_origin
import json,os,re
import sys
from langchain_core.output_parsers import JsonOutputParser
from controllers.validateapi import validateApi
from controllers.storefiles import storageUtils,json_to_doc,vector_search,vector_node_list,vector_delete,vector_create_db,vector_node_list_query,vector_update_db
from controllers.insertProject import insertProject
from pymongo import MongoClient
from io import BytesIO
from dotenv import load_dotenv
from Types.Error import SUCESS,FAILED,NAMEERROR,PROJECTNAMEERROR,VECTORSERACHERROR
load_dotenv()
sys.path.insert(0,"/Users/arun/Documents/GitHub/4dcloudapis/")
from FDStore.FDStore import FDVectorStore
URL = os.getenv("FDSTORE_URL")
PASSWORD = os.getenv("PASSWORD")
DBUSERNAME = os.getenv("DBUSERNAME")
UNAUTHORIZED = {"status":200,"matches":"User not authorized"} 
app = Flask(__name__)
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = "/datasetupload"
Mongoconnection = MongoClient("mongodb://localhost:27017/")
print(DBUSERNAME)
@app.route('/insertvector',methods=["post"])
@cross_origin()
def insert_vector_by_file():
   if validateApi(request,Mongoconnection)  :
      if storageUtils(request,projectid=request.form.get("projectid")) : 
          return {"status":200,"upserted":True}
   return {"status":400,"upserted":False}
@app.route("/apis/createProject",methods=["POST"])
@cross_origin()
def createProject():
   try :
       FDVectorConnection = FDVectorStore(URL,DBUSERNAME,PASSWORD,"")
       if validateApi(request,Mongoconnection)  :
         name = request.get_json()
         if re.search("^[0-9\W]",name["projectname"])  == None and name["projectname"] != "":
             vector_create_db(name,FDVectorConnection)
             insertProject(request,Mongoconnection,name)
             return SUCESS
         else :
            return  NAMEERROR
       else :
          return UNAUTHORIZED
   except Exception as error:
       ex_type, ex_value, ex_traceback = sys.exc_info()
       return jsonify({"status":400,"creation":False,"message":error.message})

@app.route("/apis/insertvector_json",methods=["post"])
@cross_origin()
def insert_by_json():
   if validateApi(request,Mongoconnection):
      body = request.get_json()
      isProjectExisits = list(filter(lambda value : value["id"] == body["projectid"],request.userdata["projects"]))
      print("45",len(list(isProjectExisits))>0)
      if len(isProjectExisits)>0 :
              doc = json_to_doc(request)
              FDVectorConnection = FDVectorStore(URL,DBUSERNAME,PASSWORD,body["projectid"])
              if FDVectorConnection.FDStoreAdd(docs=doc,database=body["projectid"]):
                 return {"status":200,"upserted":True}
      else :
         return PROJECTNAMEERROR
   else :
      return {"status":200,"message":"User not authorized"} 
   return FAILED

@app.route("/apis/search_vector",methods=["post"])
@cross_origin()
def search_vector():
    if validateApi(request,Mongoconnection):
      name = request.get_json()
      FDVectorConnection = FDVectorStore(URL,DBUSERNAME,PASSWORD,name["projectid"])
      result = vector_search(request,FDVectorConnection) 
      print(result)
      if result and len(result)>0:
         return result 
      else :
         return VECTORSERACHERROR
    else :
          return {"status":200,"matches":"User not authorized"} 
    
@app.route("/apis/list_node",methods=['post'])
@cross_origin()
def list_node():
    try :
        if validateApi(request,Mongoconnection):
           body = request.get_json()
           projectid = body["projectid"]
           pagination = body["pagination"]
           limit = body["limit"]
           FDVectorConnection = FDVectorStore(URL,DBUSERNAME,PASSWORD,projectid)
           result = vector_node_list(request,FDVectorConnection,limit,pagination)
           return result
        else :
           return {"status":200,"matches":"User not authorized"}
    except Exception as Error:
       return VECTORSERACHERROR
@app.route("/apis/list_node_by_query",methods=['post'])
@cross_origin()
def list_node_query():
    try :
        if validateApi(request,Mongoconnection):
           body = request.get_json()
           projectid = body["projectid"]
           fieldname = body["field"]
           value = body["value"]
           limit = body["limit"]
           FDVectorConnection = FDVectorStore(URL,DBUSERNAME,PASSWORD,projectid)
           result = vector_node_list_query(request,FDVectorConnection,fieldname,value,limit)
           return result
        else :
           return {"status":200,"matches":"User not authorized"}
    except Exception as Error:
       print(Error)
       return VECTORSERACHERROR
@app.route("/apis/delete_node",methods=["post"])
@cross_origin()
def delete_by_select():
   if validateApi(request,Mongoconnection):
      try :
          body = request.get_json()
          projectid = body["projectid"]
          fieldname = body["field"]
          value = body["value"]
          FDVectorConnection = FDVectorStore(URL,DBUSERNAME,PASSWORD,projectid)
          result  = vector_delete(request,FDVectorConnection,fieldname,value)
          return {"status":200,"message":"Deleted"}
      except Exception as Error :
          print(Error)
          return {"status":200,"message":"Delete Failed!"}
   else :
      return {"status":200,"matches":"User not authorized"}
@app.route("/apis/update_node",methods=["post"])
@cross_origin()
def update_by_select():
   if validateApi(request,Mongoconnection):
      try :
          body = request.get_json()
          projectid = body["projectid"]
          fieldname = body["field"]
          value = body["value"]
          embedding = body["embedding"]
          FDVectorConnection = FDVectorStore(URL,DBUSERNAME,PASSWORD,projectid)
          result  = vector_update_db(FDVectorConnection,fieldname,value,embedding)
          return {"status":200,"message":"Updated"}
      except Exception as Error :
          print(Error)
          return {"status":200,"message":"Update Failed!"}
   else :
      return {"status":200,"matches":"User not authorized"}


if __name__ == '__main__':
   app.run(debug=False)