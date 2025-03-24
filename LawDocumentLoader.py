from typing import Iterator
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

import re

def extract_paragraph_info(text):
    pattern = r"§\s*(\d+[a-z]?)\s*([A-Za-z]+)?\s*:\s*(.*)"
    match = re.match(pattern, text)
    
    if match:
        # Extract info (title, abbrevation, identifier)
        parag_number = match.group(1)
        law_abbreviation = match.group(2) if match.group(2) else "Kein Kürzel"
        title = match.group(3)
        
        return {
            "paragraph": parag_number,
            "law": law_abbreviation,
            "title": title
        }
    else:
        return None

class LawDocumentLoader(BaseLoader):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.lastdoc = None

    def lazy_load(self) -> Iterator[Document]:
        with open(self.file_path, encoding="utf-8") as f:
            info = {}
            content = ""
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    if len(content) > 0 and info is not None and info != self.lastdoc:
                        page = f"§ {info['paragraph']} {info['law']}: {info['title']}\n{content}"
                        yield Document(
                            page_content=page,
                            metadata=info
                        ) 
                    content = ""
                    self.lastdoc = info
                    continue
                if line.startswith("§"):
                    info = extract_paragraph_info(line)
                else:
                    content = " ".join([content, line])