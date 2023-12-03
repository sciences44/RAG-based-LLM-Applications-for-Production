"""
This class is here to manage the lifecycle of the data. Download, cleaning etc.
"""

from RAGbasedLLMApplicationsforProduction import config
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional
from pydantic import BaseModel
import ray

from bs4 import BeautifulSoup, NavigableString
from langchain.text_splitter import RecursiveCharacterTextSplitter


class Data(BaseModel):
    """
    This is the base class for all the data that is going to be passed to the agent.
    """
    
    timestamp: datetime = datetime.now() # When the data has been ingested
    raw_dataset: Optional[ray.data.dataset.MaterializedDataset] = None


    def load_data(self) -> ray.data.dataset.MaterializedDataset:
        # Ray dataset
        DOCS_DIR = Path(config.get("data",'data_path'), "docs.ray.io/en/master/")
        self.raw_dataset = ray.data.from_items([{"path": path} for path in DOCS_DIR.rglob("*.html") if not path.is_dir()])
    
    def _extract_text_from_section(self, section):
        texts = []
        for elem in section.children:
            if isinstance(elem, NavigableString):
                if elem.strip():
                    texts.append(elem.strip())
            elif elem.name == "section":
                continue
            else:
                texts.append(elem.get_text().strip())
        return "\n".join(texts)

    def _path_to_uri(self, path, scheme="https://", domain="docs.ray.io"):
        return scheme + domain + str(path).split(domain)[-1]



    def extract_sections(self, record):
        with open(record["path"], "r", encoding="utf-8") as html_file:
            soup = BeautifulSoup(html_file, "html.parser")
        sections = soup.find_all("section")
        section_list = []
        for section in sections:
            section_id = section.get("id")
            section_text = self._extract_text_from_section(section)
            if section_id:
                uri = self._path_to_uri(path=record["path"])
                section_list.append({"source": f"{uri}#{section_id}", "text": section_text})
        return section_list


    def chunk_section(self, section, size, overlap):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=size,
            chunk_overlap=overlap,
            length_function=len
            )

        chunks = text_splitter.create_documents(
            texts=[section["text"]], 
            metadatas=[{"source": section["source"]}]
            )
        
        return [{"text": chunk.page_content, "source": chunk.metadata["source"]} for chunk in chunks]

    class Config:
        arbitrary_types_allowed = True