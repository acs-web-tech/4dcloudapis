from langchain_community.document_loaders import WebBaseLoader
def WebPageLoader(urls=[]):
    loader = WebBaseLoader(urls)
    docs = loader.aload()
    return docs