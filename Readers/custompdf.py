from io import BytesIO
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders.blob_loaders import Blob
from langchain_core.documents import Document
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Union,
)
class CustomPDFLoader(BaseLoader):
    def __init__(self, stream: BytesIO, password: Optional[Union[str, bytes]] = None, extract_images: bool = False):
        self.stream = stream
        self.parser = PyPDFParser(password=password, extract_images=extract_images)

    def load(self) -> List[Document]:
        blob = Blob.from_data(self.stream.getvalue())
        return list(self.parser.parse(blob))
    