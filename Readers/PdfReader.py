from DynamicParams.dynamicParams import setParams
def PdfDataLoader(**kargs) :
    from io import BytesIO
    from langchain.document_loaders import PyPDFLoader
    from PyPDF2 import PdfReader
    source = None
    reader = None
    paramItems = kargs.items()
    params = dict(setParams(paramItems))
    if 'url' in params and params['url'] is not None:
        source = params['url']
        reader = PyPDFLoader(source).load()
    elif 'buffer' in params and params['buffer'] is not None:
        source = BytesIO(params['buffer'])
        reader = PdfReader(source)
    else:
        raise ValueError("Either 'url' or 'buffer' must be provided and not None")
    return reader

    
    

