def ExcelReader(source,mapping=[],unique_id_gen=False,doc_id=None,meta_include=[],make_embedding=""):
    import pandas
    import json
    from DynamicParams.ConvertDocument import converToDocument
    from DynamicParams.Crptosecrets import GenerateUniqueId
    if source != None:
      if len(mapping)>0:
        file = pandas.read_excel(source,names=mapping)
      else : 
        file = pandas.read_excel(source)
      if len(mapping) == len(file.keys()):
        data = file.to_json(orient="records")
        data=list(json.loads(data))
        doc = converToDocument(data,file.keys(),unique_id_gen or GenerateUniqueId,doc_id,meta_include=meta_include,make_embedding=make_embedding)
      return doc
    return None