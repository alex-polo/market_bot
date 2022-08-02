from loguru import logger
import os
import traceback
from config import load_config, LoggerConfig
from app import start_main


def configure_logger(config: LoggerConfig):
    logger.add(
        os.path.join(os.path.dirname(__file__), config.logger_dir + '/' + config.logger_filename),
        format=config.logger_format,
        level=config.logger_level,
        rotation=config.logger_rotation,
        compression=config.logger_compression
    )


def _main():
    try:
        config = load_config(os.path.join(os.path.dirname(__file__), '.env'))
        configure_logger(config.logger_config)
        logger.info(f'{config.app_attr.name} starting, app version: {config.app_attr.version}')
        start_main(config=config)
    except KeyboardInterrupt:
        logger.warning('Приложение остановлено пользователем.')
    except Exception as error:
        logger.error(traceback.format_exc(limit=None, chain=True))
        logger.error(error)


if __name__ == '__main__':
    _main()
