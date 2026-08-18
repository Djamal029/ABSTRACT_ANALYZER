# Interface VectorStoreDAO : upsert/recherche/suppression de vecteurs d'embedding (implementee par Chroma aujourd'hui, pgvector au deploiement).
class VectorStoreDao:
    def __init__(self):
        pass

    def upsert(self, id_, vec, meta):
        pass

    def searchSimilar(self, vec, k, editionId):
        # editionId restricts the search to vectors upserted with that
        # editionId in meta, so a duplicate/relevance search never matches
        # an abstract from a different edition.
        pass

    def delete(self, id_):
        pass