from pydantic_settings import BaseSettings


class DevelopConfig(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    JWT_SECRET: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        from_attribute = True


settings = DevelopConfig()
