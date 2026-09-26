# Implementation EditionDAO (SQLAlchemy, compatible MySQL/Postgres).
from app.dao.interfaces.edition_dao import EditionDao
from app.dao.relational.sqlalchemy_models import EditionModel
from app.domain.models.edition import Edition

class EditionDaoImpl(EditionDao):
    def __init__(self, db):
        self.db = db

    def create(self, edition: Edition) -> Edition:
        row = EditionModel(
            editionId=edition.editionId,
            eventId=edition.eventId,
            theme=edition.theme,
            startDate=edition.startDate,
            endDate=edition.endDate,
            isClosed=edition.isClosed,
        )
        self.db.add(row)
        self.db.flush()
        return edition

    def changeEditionTheme(self, edition: Edition, newTheme: str):
        row = self.db.query(EditionModel).filter_by(editionId=edition.editionId).first()
        if row is None:
            raise Exception(f"Edition with ID {edition.editionId} not found.")
        row.theme = newTheme
        self.db.flush()

    def getById(self, editionId: str) -> Edition:
        row = self.db.query(EditionModel).filter_by(editionId=editionId).first()
        if row is None:
            raise Exception(f"Edition with ID {editionId} not found.")
        return self._toDomain(row)

    def close(self, editionId: str):
        row = self.db.query(EditionModel).filter_by(editionId=editionId).first()
        if row is None:
            raise Exception(f"Edition with ID {editionId} not found.")
        row.isClosed = True
        self.db.flush()

    def _toDomain(self, row: EditionModel) -> Edition:
        return Edition(
            row.editionId,
            row.eventId,
            row.theme,
            row.startDate,
            row.endDate,
            row.isClosed
        )