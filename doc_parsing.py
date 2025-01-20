import os
import json
import pymupdf4llm
from chonkie import TokenChunker, SentenceChunker
import tiktoken
import uuid
from sentence_transformers import SentenceTransformer
from weaviate import Client
from weaviate_manager import WeaviateManager  # Import the class

# Initialize SentenceTransformer
model = SentenceTransformer("nomic-ai/modernbert-embed-base")

def generate_embeddings(text):
    return model.encode(text).tolist()  # Convert embeddings to list


def process_pdfs(pdf_dir):
    tokenizer = tiktoken.get_encoding("gpt2")
    chunker = SentenceChunker(tokenizer)
    pdf_chunk_map = {}

    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_dir, filename)
            document_id = str(uuid.uuid4())

            md_text = pymupdf4llm.to_markdown(filepath)
            chunks = chunker(md_text)

            pdf_chunk_map[filename] = {
                "document_id": document_id,
                "chunks": [
                    {
                        "text": chunk.text,
                        "embeddings": generate_embeddings(chunk.text)  # Add embeddings
                    } for chunk in chunks
                ]
            }
    return pdf_chunk_map  # Return after processing one file

# Example usage:
pdf_directory = "pdfs"
pdf_data = process_pdfs(pdf_directory)

#Step 5: Import data to Weaviate with embeddings

 
# Assuming pdf_data contains your processed PDF information

manager = WeaviateManager("Test_Documents_2")
cl=manager.get_class()
for pdf_filename, data in pdf_data.items():
    for chunk in data["chunks"]:
        # Prepare data for Weaviate, including embeddings
        weaviate_object = {
            "title": pdf_filename,
            "content": chunk["text"],
            
            "date": "",
            "doc_id": data['document_id']
        },

        
        vector = chunk["embeddings"]

        # Import data to Weaviate
        response = cl.data.insert(data)
        print(response)
manager.close_connection()

print("Data added to Weaviate successfully!")