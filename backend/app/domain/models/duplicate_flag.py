# Entite DuplicateFlag : doublon potentiel detecte, en attente de validation humaine.
class DuplicateFlag:
    def __init__(self, duplicateFlagId, editionId, abstractAID, abstractBID, similarityScore, status):
        self.duplicateFlagId = duplicateFlagId
        self.editionId = editionId
        self.abstractAID = abstractAID
        self.abstractBID = abstractBID
        self.similarityScore = similarityScore
        self.status = status