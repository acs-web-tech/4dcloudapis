import os,sys,pathlib
from langchain_core.documents import Document
sys.path.insert(0,"/Users/arun/Documents/GitHub/4dcloudapis/")
from Types.mimetypes import GLOBAL_SUPPORTED_MIME_TYPES_EXCEL,GLOBAL_SUPPORTED_MIME_TYPES_PDF
from Readers.ExcelReader import ExcelReader
from Readers.custompdf import CustomPDFLoader
from io import BytesIO
from FDStore.FDStore import FDVectorStore
def storageUtils(request,**kargs):
    mimetype = request.files["file"].mimetype
    print(kargs)
    getConnection = default_iterator_search(request.userdata["projects"],kargs["projectid"])
    if mimetype in GLOBAL_SUPPORTED_MIME_TYPES_EXCEL:
        docs = list(ExcelReader(request.files.get("file"),**kargs))
        vector_init(docs=docs,)
    if mimetype in GLOBAL_SUPPORTED_MIME_TYPES_PDF:
        reader = CustomPDFLoader(request.files.get("file"))
        docs = reader.load()
        print(docs)
    return vector_init(url=getConnection["connection_url"],password=getConnection["password"],username="neo4j",docs=docs)
def default_iterator_search(iterative,searchValue):
    match = None
    for key in range(0,len(iterative)):
        if iterative[key]["id"] == searchValue :
            match =iterative[key]
            break
    return match
def vector_init(**kargs):
    try:
        vector_store =  FDVectorStore(kargs["url"],kargs["username"],kargs["password"])
        vector_store.FDStoreAdd(docs=kargs["docs"])
        vector_store.close()
        return True
    except :
        return False
def vector_search(request,**kargs):
    try:
        body = request.get_json()
        getConnection = default_iterator_search(request.userdata["projects"],body["projectid"])
        vector_store =  FDVectorStore(url=getConnection["connection_url"],password=getConnection["password"]
        ,username="neo4j")
        docs = vector_store.FDStorequery(searchType="similarity_search_with_score",query=body["query"],k=body["result_count"])
        array = list(map(docs_to_json,docs))
        vector_store.close()
        return array
    except :
        return False
def json_to_doc(request):
    try:
       body = request.get_json()
       print(body["concat_field"])
       docs = list(map(lambda value:Document(page_content=f"{value[body['concat_field']]} : {value[body['embeddingText']]}",metadata={body["meta_data"]:value[body["meta_data"]]}),body["dataset"]))
       getConnection = default_iterator_search(request.userdata["projects"],body["projectid"])
       return vector_init(url=getConnection["connection_url"],password=getConnection["password"],username="neo4j",docs=docs)
    except : 
        return False
def docs_to_json(doc):
    return {"matched_content":doc[0].page_content,"meta_data":doc[0].metadata,"score":doc[1]}
def vector_node_list(request):
    body = request.get_json()
    getConnection = default_iterator_search(request.userdata["projects"],body["projectid"])
    vector_store =  FDVectorStore(url=getConnection["connection_url"],password=getConnection["password"]
    ,username="neo4j")
    docs = vector_store.select_node(body["query"],body["field"])
    #array = list(map(docs_to_json,docs))
    vector_store.close()
    return docs
def vector_delete(request):
    body = request.get_json()
    getConnection = default_iterator_search(request.userdata["projects"],body["projectid"])
    vector_store =  FDVectorStore(url=getConnection["connection_url"],password=getConnection["password"]
    ,username="neo4j")
    docs = vector_store.delete(body["field"],body["query"])
    #array = list(map(docs_to_json,docs))
    vector_store.close()
    return docs