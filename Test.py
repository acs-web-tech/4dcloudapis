from Readers.PdfReader import PdfDataLoader
from Readers.ExcelReader import ExcelReader
print(list(ExcelReader("C:/Users/arun/Downloads/Online Sales Data.xls",
mapping=["S_no","name","email"],unique_id_gen=False,doc_id="S_no",meta_include=["email","name"])))