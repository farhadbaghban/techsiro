import os
import environ
from .base import *  # noqa: F403
import dj_database_url

environ.Env.read_env(Path.joinpath(BASE_DIR, "settings", ".env"))

env = environ.Env(DEBUG=(bool, False))
DEBUG = env("DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

SECRET_KEY = env("SECRET_KEY", cast=str)


PROJECT_URL_PREFIX = "api/v1/"

# Application definition
THIRD_PARTY_APPS = [
    "corsheaders",
    "django_filters",
    "drf_yasg",
    "rest_framework",
    "rest_framework_simplejwt",
]

PROJECT_APPS = [
    "projectApps.accounts.apps.AccountsConfig",
    "projectApps.products.apps.ProductsConfig",
    "projectApps.comments.apps.CommentsConfig",
    "projectApps.cart.apps.CartConfig",
]

INSTALLED_APPS += THIRD_PARTY_APPS  # noqa: F405
INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Database Configuration
DATABASES = {
    "default": dj_database_url.config(
        default=f'postgres://{env("DB_USER_USERNAME", cast=str)}:{env("DB_USER_PASSWORD", cast=str)}@{env("DB_HOST", cast=str)}:{env("DB_PORT", cast=int)}/{env("DB_NAME", cast=str)}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Redis configuration
REDIS_HOST = os.environ.get("REDIS_HOST", "techsiro_cache")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_DB = os.environ.get("REDIS_DB", "0")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# Cache configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",  # Using database 1 for cache
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Celery configuration
CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
)  # Using database 0 for broker
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
)  # Using database 0 for results
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),  # noqa: F405
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),  # noqa: F405
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(hours=1),  # noqa: F405
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=30),  # noqa: F405
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # noqa: F405
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # noqa: F405
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")  # noqa: F405
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}
