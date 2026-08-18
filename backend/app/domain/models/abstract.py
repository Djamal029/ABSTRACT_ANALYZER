class Abstract:
    def __init__(self, abstractId, editionId, authorId, abstractTitle, abstractText,
                 keywords, status, relevanceScore, embeddingId, submittedAt):
        self.abstractId = abstractId
        self.editionId = editionId
        self.authorId = authorId
        self.abstractTitle = abstractTitle
        self.abstractText = abstractText
        self.keywords = keywords  # list[str], optional. Author-submitted, used for
        # lexical duplicate comparison and dashboard filtering, not fed into the
        # embedding (EmbeddingService only concatenates title + text for SPECTER2).
        self.status = status
        self.relevanceScore = relevanceScore
        self.embeddingId = embeddingId
        self.submittedAt = submittedAt
