from pathlib import Path
import chromadb
from sympy import re


def charger_documents():
    """" Lit tous les ficies du dossier doocs et renvoie leur contenu"""
    documents =[]
    dossier = Path("docs")


    for fichier in dossier.glob("*.txt"):
        texte = fichier.read_text(encoding="utf-8")
        documents.append({
            "source": fichier.name,
            "texte": texte,
        })
    return documents


def contruire_base():
    """ Range les documents dans Chroma"""
    documetns = charger_documents()
    client = chromadb.EphemeralClient()
    collection = client.create_collection(name="documents")

    collection.add(
            documents=[d["texte"] for d in documetns],
            metadatas=[{"source": d["source"]} for d in documetns],
            ids=[f"doc_{i}" for i in range(len(documetns))]
    )
    return collection

def chercher(collection, question, k=3):
    return collection.query(
        query_texts=[question],
        n_results=k
    )

if __name__ == "__main__":
    collection = contruire_base()
    print(f"Base construite avec {collection.count()} documents")
    question = "est ce que je peux travailler chez moi"    
    resultats = chercher(collection, question)

    print(f"\nQuestion : {question}")
    for texte, meta in zip(resultats["documents"][0], resultats["metadatas"][0]):
        print(f"\n--- Trouvé dans {meta['source']} ---")
        print(texte)