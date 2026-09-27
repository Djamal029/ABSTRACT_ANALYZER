# Entite DuplicateFlag : doublon potentiel detecte, en attente de validation humaine.
class DuplicateFlag:
    def __init__(self, duplicateFlagId, editionId, abstractAID, abstractBID,
                 similarityScore, status):
        self.duplicateFlagId = duplicateFlagId
        self.editionId = editionId
        self.abstractAID = abstractAID
        self.abstractBID = abstractBID
        self.similarityScore = similarityScore
        self.status = status

    # get the similarity score rounded to 2 decimal places
    def getSimilarityPercentage(self):
        return round(self.similarityScore, 2)

    # Get status as a human-readable string
    def getStatusString(self):
        if self.status == "PENDING":
            return "Pending"
        elif self.status == "CONFIRMED":
            return "Confirmed"
        elif self.status == "REJECTED":
            return "Rejected"
        else:
            return "Unknown"

    # Get the two abstract IDs as a tuple
    def getAbstractIDs(self):
        return (self.abstractAID, self.abstractBID)
