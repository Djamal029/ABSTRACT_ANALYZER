# Configuration centralisee (Pydantic Settings) : choix des implementations DAO/provider (MySQL/Postgres, Chroma/pgvector, SPECTER2/autre) injectees dans le reste de l'app.
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwtSecretKey: str | None = Field(default=None, validation_alias="JWT_SECRET_KEY")
    accessTokenExpireMinutes: int = Field(default=30, gt=0)
    databaseUrl: str = "mysql+pymysql://root:@localhost:3306/abstract_analyzer"


settings = Settings()