# passwordHash : jamais le mot de passe en clair, hash calcule par core/security.py
class User:
    def __init__(self, userId, userEmail, userFullName, userRole, passwordHash, isActive, createdAt):
        self.userId = userId
        self.userEmail = userEmail
        self.userFullName = userFullName
        self.userRole = userRole
        self.passwordHash = passwordHash
        self.isActive = isActive
        self.createdAt = createdAt