"""
Thos module have the agent which is doing important task to faciliate the RAG such as extraction, integration etc.
"""
from RAGbasedLLMApplicationsforProduction import config
from RAGbasedLLMApplicationsforProduction.data import Data
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional
from pydantic import BaseModel
import ray

from functools import partial


class agent(BaseModel):
    """.

    Args:
        datetime: timestamp.

    Returns:
        float: a.
    """
    timestamp: datetime = datetime.now()
    # data: Optional[Data] = None


    def load_html_data(self):
        data= Data()
        data.load_data()
        return data.raw_dataset.flat_map(data.extract_sections)

    def extract_chunk_from_section(self, section_list, chunk_size, chunk_overlap):
        return section_list.flat_map(partial(
            Data().chunk_section,
            size=chunk_size,
            overlap=chunk_overlap
            ))

    
        


    def context(self):
        print(config.get('vectordb', 'url'))
        





