from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.dao.relational.mysql_abstract_dao import MySQLAbstractDAO
from app.dao.relational.sqlalchemy_models import AbstractModel, Base
from app.domain.enums import Enums
from app.domain.exceptions import AbstractWithdrawn


@pytest.fixture
def dao_and_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    session.add_all(
        [
            AbstractModel(
                abstractId="active-id",
                editionId="edition-id",
                authorId="author-id",
                abstractTitle="Active abstract",
                abstractText="Text",
                keywords=[],
                status=Enums.AbstractStatus.SUBMITTED,
                relevanceScore=0.82,
                embeddingId="active-vector",
                submittedAt=datetime(2026, 1, 1),
            ),
            AbstractModel(
                abstractId="withdrawn-id",
                editionId="edition-id",
                authorId="author-id",
                abstractTitle="Withdrawn abstract",
                abstractText="Historical text",
                keywords=[],
                status=Enums.AbstractStatus.WITHDRAWN,
                relevanceScore=0.91,
                embeddingId="historical-vector",
                submittedAt=datetime(2026, 1, 2),
            ),
        ]
    )
    session.flush()
    yield MySQLAbstractDAO(session), session
    session.close()
    engine.dispose()


def test_operational_list_excludes_withdrawn_but_history_keeps_it(dao_and_session):
    dao, _ = dao_and_session

    active = dao.listByEdition("edition-id")
    history = dao.listAllByEdition("edition-id")

    assert [abstract.abstractId for abstract in active] == ["active-id"]
    assert {abstract.abstractId for abstract in history} == {"active-id", "withdrawn-id"}


def test_withdraw_preserves_existing_score_and_embedding(dao_and_session):
    dao, _ = dao_and_session

    dao.withdraw("active-id")
    withdrawn = dao.getById("active-id")

    assert withdrawn.status == Enums.AbstractStatus.WITHDRAWN
    assert withdrawn.relevanceScore == 0.82
    assert withdrawn.embeddingId == "active-vector"
    assert dao.listByEdition("edition-id") == []


def test_withdrawn_abstract_cannot_receive_a_new_relevance_score(dao_and_session):
    dao, _ = dao_and_session

    with pytest.raises(AbstractWithdrawn):
        dao.updateRelevanceScore("withdrawn-id", 0.99)

    assert dao.getById("withdrawn-id").relevanceScore == 0.91
