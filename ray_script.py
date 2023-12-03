import ray
from ray.data import ActorPoolStrategy

from datetime import datetime
from pathlib import Path
from RAGbasedLLMApplicationsforProduction import config
from RAGbasedLLMApplicationsforProduction.app import agent
from RAGbasedLLMApplicationsforProduction.embed import EmbedChunks
ray.init()
import certifi
print(certifi.where())
# ------------------------------------------------------------------------
# ------------------------ Chunk data ------------------------------------
# --------------------


# ------------------------ Loading the data  ----------------------------
myAgent = agent()
extract_sections = myAgent.load_html_data()
# ------------------------ Plot size of the sections to watch 👀 [Remove in prod]  ----------------------------
import matplotlib.pyplot as plt
section_lengths = []
for section in extract_sections.take_all():
    section_lengths.append(len(section["text"]))

plt.figure(figsize=(12, 3))
plt.plot(section_lengths, marker='o')
plt.title("Section lengths")
plt.ylabel("# chars")
plt.savefig(Path(config.get("data","data_path")+'/sections_char.png'))

# ------------------------ Langchain ----------------------------

chunk_size = 300
chunk_overlap = 50

chunk_section = myAgent.extract_chunk_from_section(section_list=extract_sections, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
print("\n\n"+f"{chunk_section.count()} chunks + \n\n\n")
print("\n\n\n")
print(type({chunk_section}))
print("\n\n\n")
chunk_section.show(1)

# ------------------------ Plot size of the sections to watch 👀 [Remove in prod]  ----------------------------
import matplotlib.pyplot as plt
section_lengths = []
for section in chunk_section.take_all():
    section_lengths.append(len(section["text"]))

plt.figure(figsize=(12, 3))
plt.plot(section_lengths, marker='o')
plt.title("Section lengths")
plt.ylabel("# chars")
plt.savefig(Path(config.get("data","data_path")+'/sections_divider_chunk_char.png'))

# ------------------------------------------------------------------------
# ------------------------ Embedding ------------------------------------
# --------------------

# Embed chunks
embedding_model_name = "thenlper/gte-base"
embedded_chunks = chunk_section.map_batches(
    EmbedChunks,
    fn_constructor_kwargs={"model_name": embedding_model_name},
    batch_size=100, 
    num_gpus=0,
    compute=ActorPoolStrategy(size=2))

# Sample
sample = embedded_chunks.take(1)
print ("embedding size:", len(sample[0]["embeddings"]))
print (sample[0]["text"])

# ------------------------------------------------------------------------
# ------------------------ Index data ------------------------------------
# --------------------



ray.shutdown()
