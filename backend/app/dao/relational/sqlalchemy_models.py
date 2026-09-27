# ORM tables (SQLAlchemy). These mirror the domain entities in domain/models/
# but are NOT the same objects: a *Model class is a table row, a domain class
# is a plain business object with no SQLAlchemy dependency. DAO implementations
# convert between the two; no other layer ever imports from this file.
from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class EditionModel(Base):
    __tablename__ = "editions"
    editionId = Column(String(36), primary_key=True)
    editionName = Column(String(255), nullable=False)
    editionTheme = Column(String(2000), nullable=False)
    themeEmbeddingId = Column(String(64))
    submissionsOpenAt = Column(DateTime)
    submissionStartAt = Column(DateTime)
    status = Column(String(20), nullable=False)


class UserModel(Base):
    __tablename__ = "users"
    userId = Column(String(36), primary_key=True)
    userEmail = Column(String(255), nullable=False, unique=True)
    userFullName = Column(String(255), nullable=False)
    userRole = Column(String(20), nullable=False)
    passwordHash = Column(String(255), nullable=False)
    isActive = Column(String(1), nullable=False, default="1")
    createdAt = Column(DateTime, nullable=False)


class AbstractModel(Base):
    __tablename__ = "abstracts"
    abstractId = Column(String(36), primary_key=True)
    editionId = Column(String(36), ForeignKey("editions.editionId"), nullable=False)
    authorId = Column(String(36), ForeignKey("users.userId"), nullable=False)
    abstractTitle = Column(String(500), nullable=False)
    abstractText = Column(String(8000), nullable=False)
    keywords = Column(JSON)  # list[str], optional
    status = Column(String(20), nullable=False)
    relevanceScore = Column(Float)
    embeddingId = Column(String(64))
    submittedAt = Column(DateTime, nullable=False)


class ClusterModel(Base):
    __tablename__ = "clusters"
    clusterId = Column(String(36), primary_key=True)
    editionId = Column(String(36), ForeignKey("editions.editionId"), nullable=False)
    clusterName = Column(String(255))
    clusterKeyWords = Column(JSON)  # list[str], no separate join table needed
    clusterEmbeddingId = Column(String(64))
    status = Column(String(20), nullable=False)


class DuplicateFlagModel(Base):
    __tablename__ = "duplicate_flags"
    duplicateFlagId = Column(String(36), primary_key=True)
    editionId = Column(String(36), ForeignKey("editions.editionId"), nullable=False)
    abstractAID = Column(String(36), ForeignKey("abstracts.abstractId"), nullable=False)
    abstractBID = Column(String(36), ForeignKey("abstracts.abstractId"), nullable=False)
    similarityScore = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)


class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    auditLogId = Column(String(36), primary_key=True)
    # actorId has no ForeignKey constraint on purpose: it stays NULL for
    # system/job actions (e.g. RUN_CLUSTERING), and a log entry must survive
    # even if the user row is later deactivated/removed.
    actorId = Column(String(36), nullable=True)
    action = Column(String(50), nullable=False)
    entityType = Column(String(50), nullable=False)
    entityId = Column(String(36), nullable=False)
    # "metadata" is reserved on Base (Base.metadata), so the Python attribute
    # is named extraData while the actual DB column stays named "metadata".
    extraData = Column("metadata", JSON)
    createdAt = Column(DateTime, nullable=False)
