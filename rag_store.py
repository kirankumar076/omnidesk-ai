import chromadb 

chroma_client=chromadb.PersistentClient(path="./omnidesk_db")
collection=chroma_client.get_or_create_collection(name="company_policies")

def chunker(text:str , chunk_size : int, overlap : int)->list[str]:
    """slices a long document into overlapping text chunks."""
    chunks=[]
    step=chunk_size-overlap
    for i in range(0,len(text),step):
        chunks.append(text[i:i+chunk_size])
    return chunks

def file_loader(file_path:str , category :str ):
    """"reads a policy file from disk , chunks it and stores it in chromaDB with metadata. """
    with open(file_path,"r") as file :
        full_text=file.read()
    chunks=chunker(full_text,chunk_size=350, overlap=50)

    ids=[]
    metadatas=[]
    for i in range(len(chunks)):
        ids.append(f"{category}_{i}")
        metadatas.append({"category":category})

    collection.upsert(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )
    print(f"successfully ingested{len(chunks)} chunks from '{file_path}' [category:{category}]")

def retrival(question :str ,category:str) -> str:
    """searches the company policy database for a given question and category('shipping' or 'refunds')."""
    res=collection.query(
        query_texts=[question],
        n_results=2,
        where={"category":category}
    )
    return "\n\n".join(res["documents"][0])

