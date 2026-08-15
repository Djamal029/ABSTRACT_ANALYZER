# Entite Edition : une occurrence d'evenement (theme, fenetre de soumission, dates).
class Edition:
    def __init__(self, editionId, editionName, editionTheme, themeEmbeddingId, submissionsOpenAt, submissionStartAt, status):
        self.editionId = editionId
        self.editionName = editionName
        self.editionTheme = editionTheme
        self.themeEmbeddingId = themeEmbeddingId
        self.submissionsOpenAt = submissionsOpenAt
        self.submissionStartAt = submissionStartAt
        self.status = status
