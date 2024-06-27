from DynamicParams.dynamicParams import setParams
def PdfDataLoader(**kargs) :
    from io import BytesIO
    from langchain.document_loaders import PyPDFLoader
    from PyPDF2 import PdfReader
    source = None
    reader = None
    paramItems = kargs.items()
    params = dict(setParams(paramItems))
    if kargs.url:
        source = kargs.url
        reader = PyPDFLoader(source).load()
    else:
        raise ValueError("Either 'url' or 'buffer' must be provided and not None")
    return reader

    

