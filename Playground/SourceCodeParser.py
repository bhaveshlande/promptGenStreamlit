"""Helper to use LanguageParser"""

import warnings

warnings.filterwarnings("ignore")
from pprint import pprint
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser

loader = GenericLoader.from_filesystem(
    "evaluate.py",
    glob="*",
    parser=LanguageParser(language=Language.PYTHON)
)
docs = loader.load()
for document in docs:
    print(document.metadata)