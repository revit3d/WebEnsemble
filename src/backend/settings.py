from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRESQL_HOST: str

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        """Produce a db URI from settings"""
        return (
            "postgresql://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRESQL_HOST}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = '.temp.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = 'ignore'


settings = EnvSettings()
