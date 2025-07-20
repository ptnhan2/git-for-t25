from langchain_text_splitters import MarkdownHeaderTextSplitter
import tiktoken
from pathlib import Path

header_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5"),
    ("######", "Header 6"),
]

all_chunks = []

md_folder = Path("../md_output")
for md_file in md_folder.glob("*.md"):
    with open(md_file, "r", encoding="utf-8") as f:
        markdown_document = f.read()
        markdown_splitter = MarkdownHeaderTextSplitter(header_to_split_on)
        md_header_splits = markdown_splitter.split_text(markdown_document)
        all_chunks.extend(md_header_splits)

# print(all_chunks)


# # Print the number of tokens in each chunk
# encoding = tiktoken.encoding_for_model("text-embedding-3-small")
# for i, doc in enumerate(all_chunks):
#     tokens = encoding.encode(doc.page_content)
#     print(f"Chunk {i+1}: {len(tokens)} tokens")
#     print(f"Headers: {doc.metadata}")
#     # print(f"Content:\n{doc.page_content[:200]}...\n{'-'*60}\n")