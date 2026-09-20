from uuid import UUID
from app.domain.enums import Enums

EditionStatus = Enums.EditionStatus


class Edition:
    """Represents a single scientific edition or call-for-papers event.

    The edition owns the thematic context used to evaluate submission relevance,
    the embedding identifier for that theme, and the lifecycle state of the event.
    """

    def __init__(
        self,
        id: UUID,
        editionId: str,
        theme: str,
        themeEmbeddingId: str,
        status: str = EditionStatus.OPEN,
    ):
        """Create a new edition.

        Args:
            id: Unique database identifier.
            editionId: Business identifier used across the application.
            theme: The thematic focus of the edition.
            themeEmbeddingId: Vector storage identifier for the theme embedding.
            status: Lifecycle state of the edition.
        """
        if not isinstance(id, UUID):
            raise TypeError("id must be a UUID instance.")

        if not isinstance(editionId, str) or not editionId.strip():
            raise ValueError("editionId must be a non-empty string.")

        if not isinstance(theme, str) or not theme.strip():
            raise ValueError("theme must be a non-empty string.")

        if not isinstance(themeEmbeddingId, str) or not themeEmbeddingId.strip():
            raise ValueError("themeEmbeddingId must be a non-empty string.")

        valid_statuses = (
            EditionStatus.OPEN,
            EditionStatus.CLOSED,
            EditionStatus.CLUSTERED,
        )
        if not isinstance(status, str) or status not in valid_statuses:
            raise ValueError(
                "status must be one of: OPEN, CLOSED, CLUSTERED"
            )

        self.id = id
        self.editionId = editionId.strip()
        self.theme = theme.strip()
        self.themeEmbeddingId = themeEmbeddingId.strip()
        self.status = status

