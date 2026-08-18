# Configuration centralisee (Pydantic Settings) : choix des implementations DAO/provider (MySQL/Postgres, Chroma/pgvector, SPECTER2/autre) injectees dans le reste de l'app.
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    databaseUrl: str = "mysql+pymysql://root:@localhost:3306/abstract_analyzer"


settings = Settings()