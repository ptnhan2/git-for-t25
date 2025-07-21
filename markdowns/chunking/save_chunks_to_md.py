import os
from .data_chunking import mds_to_chunks
OUTPUT_DIR = os.path.join("markdowns","chunking", "chunking_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
def convert_chunk_to_md(chunk):   
    md = ""
    for i in range(1,6):
        key = f"Header {i}"
        if key in chunk.metadata:
            md += f"{'#' * i} {chunk.metadata[key]}\n\n"    
    md += "\n" + chunk.page_content
    return md
    

def save_chunks_markdowns(): 
    print("Saving chunks to markdown...")
    chunks = mds_to_chunks()
    print(chunks)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")
    else: 
        print(f"Directory already exists: {OUTPUT_DIR}")
    file_path = os.path.join(OUTPUT_DIR, "chunks.md")
    with open(file_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            md = convert_chunk_to_md(chunk)
            f.write(md + "\n\n ------- \n\n")        
    print(f"Saved: {file_path}")