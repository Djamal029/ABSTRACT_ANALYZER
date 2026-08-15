# Domain exceptions. All inherit from DomainError so the API layer can catch
# them generically and map them to HTTP codes in a single place, without every
# endpoint needing to know about every exception individually.

class DomainError(Exception):
    # Base class for all domain-level exceptions.
    pass


class AbstractNotFound(DomainError):
    # Raised by AbstractService when AbstractDAO.getById() finds nothing.
    pass


class EditionNotFound(DomainError):
    # Raised by EditionService when EditionDAO.getById() finds nothing.
    pass


class UserNotFound(DomainError):
    # Raised by UserService when UserDAO.getByEmail()/getById() finds nothing.
    pass


class UserAlreadyExists(DomainError):
    # Raised by UserService.register() when UserDAO.getByEmail() already
    # returns a user for the given email (unique email constraint at the
    # domain level, checked before hitting a DB unique-index error).
    pass


class EditionClosed(DomainError):
    # Raised by AbstractService.submit() if Edition.status != OPEN.
    # Blocks submission after closing, even if the API is called directly.
    pass


class DuplicateAlreadyReviewed(DomainError):
    # Raised if an organizer tries to review a DuplicateFlag whose status
    # is no longer PENDING (prevents silently overwriting an existing
    # decision without leaving a trace in the audit log).
    pass


class InvalidCredentials(DomainError):
    # Raised by core/security.py or UserService during login:
    # wrong password, or account with isActive = False.
    pass


class EditionNotClosedYet(DomainError):
    # Raised if an organizer tries to manually trigger clustering on an
    # edition that is still OPEN. The automated job only runs after closing
    # anyway; this guards an eventual manual trigger.
    pass


class UnauthorizedAction(DomainError):
    # Raised at the service level (not only the API level) when a
    # RESEARCHER attempts an action reserved for an ORGANIZER (reviewing a
    # duplicate, closing an edition...). Redundant with HTTP-layer access
    # control, but deliberate: the service must never rely solely on the
    # API layer to enforce this rule.
    pass
