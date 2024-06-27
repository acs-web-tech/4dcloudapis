import sys
import re
sys.path.insert(0,"/Users/arun/Documents/GitHub/4dcloudapis/")
from Types.mimetypes import GLOBAL_SUPPORTED_MIME_TYPES_EXCEL,GLOBAL_SUPPORTED_MIME_TYPES_PDF
def validateApi(request,connection):
    token = request.headers.get("4dcloud-auth-token")
    if token :
        cursor = connection["4dapis"]["clients"].find_one({"secrets":token},{"projects":1,"username":1})
        request.userdata = cursor
        print(cursor)
        return len(cursor["projects"])>0

def filevalidate(request):
    mimetype = request.files.get("file").mimetype
    return mimetype in GLOBAL_SUPPORTED_MIME_TYPES_EXCEL or mimetype in GLOBAL_SUPPORTED_MIME_TYPES_PDF 
