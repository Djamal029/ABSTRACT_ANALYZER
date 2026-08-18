# Implementation AbstractDAO sur MySQL (actuelle). Bridges AbstractModel (SQL row)
# <-> Abstract (domain object). No other layer ever imports AbstractModel directly.
#
# Note on transactions: this DAO never calls db.commit(). It only add()s /
# mutates objects on the session (flush() when the caller needs the write
# visible within the same transaction, e.g. to chain a query right after).
# Committing is the API layer's responsibility (see api/deps.py) so a whole
# request -- which may call several DAO methods -- succeeds or fails as one
# transaction, instead of partially persisting on a mid-request failure.
from app.dao.interfaces.abstract_dao import AbstractDAO
from app.dao.relational.sqlalchemy_models import AbstractModel
from app.domain.models.abstract import Abstract
from app.domain.exceptions import AbstractNotFound


class MySQLAbstractDAO(AbstractDAO):
    def __init__(self, db):
        super().__init__(db)

    def create(self, abstract: Abstract) -> Abstract:
        row = AbstractModel(
            abstractId=abstract.abstractId,
            editionId=abstract.editionId,
            authorId=abstract.authorId,
            abstractTitle=abstract.abstractTitle,
            abstractText=abstract.abstractText,
            keywords=abstract.keywords,
            status=abstract.status,
            relevanceScore=abstract.relevanceScore,
            embeddingId=abstract.embeddingId,
            submittedAt=abstract.submittedAt,
        )
        self.db.add(row)
        self.db.flush()
        return abstract

    def getById(self, abstractId: str) -> Abstract:
        row = self.db.query(AbstractModel).filter_by(abstractId=abstractId).first()
        if row is None:
            raise AbstractNotFound(abstractId)
        return self._toDomain(row)

    def listByEdition(self, editionId: str) -> list[Abstract]:
        rows = self.db.query(AbstractModel).filter_by(editionId=editionId).all()
        return [self._toDomain(row) for row in rows]

    def updateStatus(self, abstractId: str, status: str):
        row = self.db.query(AbstractModel).filter_by(abstractId=abstractId).first()
        if row is None:
            raise AbstractNotFound(abstractId)
        row.status = status
        self.db.flush()

    def updateRelevanceScore(self, abstractId: str, relevanceScore: float):
        row = self.db.query(AbstractModel).filter_by(abstractId=abstractId).first()
        if row is None:
            raise AbstractNotFound(abstractId)
        row.relevanceScore = relevanceScore
        self.db.flush()

    def _toDomain(self, row: AbstractModel) -> Abstract:
        return Abstract(
            row.abstractId,
            row.editionId,
            row.authorId,
            row.abstractTitle,
            row.abstractText,
            row.keywords,
            row.status,
            row.relevanceScore,
            row.embeddingId,
            row.submittedAt,
        )
