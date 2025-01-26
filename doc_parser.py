# Import necessary libraries
import pymupdf4llm
import pandas as pd
import uuid
import pathlib
from chonkie import SentenceChunker
from autotiktokenizer import AutoTikTokenizer
from sentence_transformers import SentenceTransformer

# Initialize tokenizer and model
tokenizer = AutoTikTokenizer.from_pretrained("gpt2")
model = SentenceTransformer("nomic-ai/modernbert-embed-base")

# Create a SentenceChunker instance
chunker = SentenceChunker(
    tokenizer="gpt2",  # Supports string identifiers
    chunk_size=512,  # Maximum tokens per chunk
    chunk_overlap=128,  # Overlap between chunks
    min_sentences_per_chunk=1  # Minimum sentences in each chunk
)

# Directory containing PDF files
pdf_dir = pathlib.Path("pdfs")

# List to store data for DataFrame
data = []

# Process each PDF file in the directory
for pdf_file in pdf_dir.glob("*.pdf"):
    # Load the PDF file
    md_text = pymupdf4llm.to_markdown(pdf_file)
    data.append({
        "doc_id": str(uuid.uuid4()),
        "Title": pdf_file.name if pdf_file.name else "Untitled",
        "Content": md_text,  # Markdown text content
    })

# Create a DataFrame
df = pd.DataFrame(data)

# Define a function to process the content column
def process_content(content):
    chunks = chunker.chunk(content)
    return ((chunk.text, len(chunk.sentences)) for chunk in chunks)

# Apply the function to the content column and expand the DataFrame
expanded_data = []
for _, row in df.iterrows():
    processed_content = process_content(row['Content'])
    for text, count in processed_content:
        expanded_data.append({
            "doc_id": row['doc_id'],
            "Title": row['Title'],
            "Original Content": row['Content'],
            "Chunk": text.strip(),
            "Chunk Length": count
        })

# Create DataFrame with the expanded data
# Create a new DataFrame with the expanded data
expanded_df = pd.DataFrame(expanded_data)

# Define a function to execute on the Chunk Content column
def generate_chunk_embeddings(chunk_content):
    # Add your processing logic here
    return model.encode(chunk_content).tolist()

# Apply the function to the Chunk Content column and store the result in a new column
expanded_df['Processed Chunk Embeddings'] = expanded_df['Chunk'].apply(generate_chunk_embeddings)

# Save the expanded DataFrame to an Excel file
excel_filepath = "output/output.xlsx"
expanded_df.to_excel(excel_filepath, index=False)

# Print the expanded DataFrame
print(expanded_df)
