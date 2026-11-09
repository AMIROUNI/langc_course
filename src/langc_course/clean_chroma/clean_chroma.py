import chromadb
import json

def get_collection(chroma_path: str, collection_name: str):
    client = chromadb.PersistentClient(path=chroma_path)

    collection = client.get_collection(name=collection_name)

    return collection


def check_duplicates(collection):
    seen = {}
    duplicate_ids = []

    data = collection.get(
        include=["documents", "metadatas"]
    )

    for doc_id, content, metadata in zip(
        data["ids"],
        data["documents"],
        data["metadatas"]
    ):
        key = (
            content,
            json.dumps(metadata or {}, sort_keys=True)
        )

        if key in seen:
            duplicate_ids.append(doc_id)
        else:
            seen[key] = doc_id

    print("Total documents:", len(data["ids"]))
    print("Unique documents:", len(seen))
    print("Duplicate documents:", len(duplicate_ids))

    return duplicate_ids


def delete_duplicates(collection, duplicate_ids):

    if not duplicate_ids:
        print("No duplicates found. Nothing to delete.")
        return

    collection.delete(ids=duplicate_ids)

    print(f"Deleted {len(duplicate_ids)} duplicate documents.")
    print("Remaining documents:", collection.count())




def clean_chroma_db(chroma_path, collection_name):

    # 1. Connect to ChromaDB
    collection = get_collection(
        chroma_path,
        collection_name
    )

    print("Documents before:", collection.count())

    # 2. Check duplicates
    duplicate_ids = check_duplicates(collection)

    # 3. Delete only if duplicates exist
    delete_duplicates(collection, duplicate_ids)


if __name__ == "__main__":

    clean_chroma_db(
        chroma_path="./chroma_db",
        collection_name="hybrid"
    )