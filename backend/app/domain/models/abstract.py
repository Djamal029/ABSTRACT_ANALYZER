class Abstract:
    def __init__(self, abstractId, editionId, authorId, abstractText, status, relevanceScore, embeddingId, submittedAt):
        self.abstractId = abstractId
        self.editionId = editionId
        self.authorId = authorId
        self.abstractText = abstractText
        self.status = status
        self.relevanceScore = relevanceScore
        self.embeddingId = embeddingId
        self.submittedAt = submittedAt
        pass