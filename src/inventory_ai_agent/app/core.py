import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    #variables obligatories d'entorn
    openai_api_key: str
    
    # fail-fast si hi ha variables d'entorn que no estan definides
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
os.environ["OPENAI_API_KEY"] = settings.openai_api_key