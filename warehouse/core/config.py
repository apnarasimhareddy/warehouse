from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str
    version:str
    Description:str
    database_url: str
    echo_sql: bool = True
    api_key:str

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()  # type: ignore