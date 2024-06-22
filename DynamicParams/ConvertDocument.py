def converToDocument(source,keys,unique_id_gen,doc_id,meta_include,make_embedding="Product_Name"):
    from langchain_core.documents import Document
    import json
    if len(source) == 0:
        raise ValueError("List has no Values")
    convertedDoc = map(lambda value:Document(page_content=value[make_embedding],metadata={"id":str(value[doc_id])or unique_id_gen(),
    "others":list(map(lambda meta:{meta:value[meta]},meta_include))}),source)
    return convertedDoc