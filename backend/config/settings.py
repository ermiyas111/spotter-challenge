from pathlib import Path

from shared.utils import env

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.get_env("DJANGO_SECRET_KEY", "dev-insecure-secret")
DEBUG = env.get_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = env.get_list("DJANGO_ALLOWED_HOSTS", ["*"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "routing",
    "stations",
    "shared",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.get_env("POSTGRES_DB", "spotter"),
        "USER": env.get_env("POSTGRES_USER", "spotter"),
        "PASSWORD": env.get_env("POSTGRES_PASSWORD", "spotter"),
        "HOST": env.get_env("POSTGRES_HOST", "localhost"),
        "PORT": env.get_env("POSTGRES_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROUTING_API_BASE_URL = env.get_env("ROUTING_API_BASE_URL", "https://router.project-osrm.org")
GEOCODING_API_BASE_URL = env.get_env("GEOCODING_API_BASE_URL", "https://nominatim.openstreetmap.org")
CORRIDOR_WIDTH_MILES = env.get_float("CORRIDOR_WIDTH_MILES", 5.0)
SAFETY_BUFFER_MILES = env.get_float("SAFETY_BUFFER_MILES", 25.0)

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}
