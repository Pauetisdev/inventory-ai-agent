from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    #variables obligatories d'entorn
    openai_api_key: str
    
    # Configurem com s'ha de comportar Pydantic en llegir l'entorn
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()