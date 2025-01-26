from weaviate.classes.query import Filter, MetadataQuery
from sentence_transformers import SentenceTransformer
import time
import weaviate
import weaviate.classes as wvc

model = SentenceTransformer("nomic-ai/modernbert-embed-base")

def generate_chunk_embeddings(chunk_content):
    # Add your processing logic here
    return model.encode(chunk_content).tolist()

client = weaviate.connect_to_local()
collection = client.collections.get("TestTable_3")

time.sleep(1)  # Sleep so we don't query before async indexing finishes

response = collection.query.near_vector(
    near_vector=generate_chunk_embeddings("The quick brown fox jumps over the lazy dog"),
    limit=2,
    return_metadata=wvc.query.MetadataQuery(certainty=True)
)

print(response)
print(response.objects[0].properties['text'])

client.close()