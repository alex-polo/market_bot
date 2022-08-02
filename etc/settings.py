# Режим работы бота (polling или webhook)
#bot_status = 'webhook'
bot_status = 'polling'

# Путь базы sqlite
database_path = 'data/database.db'

# Настройки Redis
redis_hostname = '89.108.103.38'
redis_port = 6379
redis_database = 0

# Логирование
logger_dir = 'logs'
logger_filename = 'server.log'
logger_format = '{time} {level} {message}'
logger_level = 'DEBUG'
logger_rotation = '100 MB'
logger_compression = 'zip'

# Название программы и версия
app_name = 'Mugen'
app_version = '0.01'
