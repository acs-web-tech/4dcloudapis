def ExcelReader(source,mapping=[]):
    import pandas
    import json
    from langchain_core.documents import Document
    from DynamicParams.ConvertDocument import converToDocument
    if source != None:
      if len(mapping)>0:
        file = pandas.read_excel(source,names=mapping)
      else : 
         file = pandas.read_excel(source)
      data = file.to_json(orient="records")
      data=list(json.loads(data))
      return data
    return None