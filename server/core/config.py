from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, FilePath


from server import __name__

defaultFolder = ("library", "thumbs", "upload")


class MongoDBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="db_")
    host: str = "localhost"
    port: int = 27017
    name: str = __name__
    username: str
    password: SecretStr

    @property
    def uri(self) -> str:
        return "mongodb://{username}:{password}@{host}:{port}".format(
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
        )


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="redis_")
    host: str = "localhost"
    port: int = 6379


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    # model_config = SettingsConfigDict()
    db: MongoDBSettings = MongoDBSettings()
    redis: RedisSettings = RedisSettings()
    secret_file: Optional[FilePath] = None
    debug_mode: bool = False
