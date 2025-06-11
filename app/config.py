import os

# Загружаем из .env (локально) и из Railway variables (в продакшене)
from dotenv import load_dotenv
load_dotenv()

# OAuth2
AMO_CLIENT_ID     = os.getenv("AMO_CLIENT_ID")
AMO_CLIENT_SECRET = os.getenv("AMO_CLIENT_SECRET")
AMO_REDIRECT_URI  = os.getenv("AMO_REDIRECT_URI")

# Поддомен без https:// и .amocrm.ru
AMO_SUBDOMAIN     = os.getenv("AMO_SUBDOMAIN")
