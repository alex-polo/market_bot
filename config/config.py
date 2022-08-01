from dataclasses import dataclass
from environs import Env

from etc import database_path, logger_dir, logger_filename, logger_format, logger_level, logger_rotation, \
    logger_compression, app_name, app_version, redis_hostname, redis_port, redis_background_database, \
    redis_tg_bot_database


@dataclass
class LoggerConfig:
    path_directory: str
    rotation: str


@dataclass
class AppAttr:
    name: str
    version: str


@dataclass
class DbConfig:
    path: str


@dataclass
class RedisConfig:
    hostname: str
    port: int
    password: str
    background_database: int
    tg_bot_database: int


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class LoggerConfig:
    logger_dir: str
    logger_filename: str
    logger_format: str
    logger_level: str
    logger_rotation: str
    logger_compression: str


@dataclass
class Config:
    app_attr: AppAttr
    tg_bot: TgBot
    db_config: DbConfig
    redis_config: RedisConfig
    logger_config: LoggerConfig


def load_config(path):
    env = Env()
    env.read_env(path)

    return Config(
        app_attr=AppAttr(name=app_name, version=app_version),
        tg_bot=TgBot(token=env.str("BOT_TOKEN"), admin_ids=list(map(int, env.list("ADMINS")))),
        db_config=DbConfig(path=database_path),
        redis_config=RedisConfig(
            hostname=redis_hostname,
            port=redis_port,
            password=env.str("REDIS_PASSWORD"),
            background_database=redis_background_database,
            tg_bot_database=redis_tg_bot_database
        ),
        logger_config=LoggerConfig(
            logger_dir=logger_dir,
            logger_filename=logger_filename,
            logger_format=logger_format,
            logger_level=logger_level,
            logger_rotation=logger_rotation,
            logger_compression=logger_compression)
    )
