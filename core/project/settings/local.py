from .base import *

DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

MIDDLEWARE = MIDDLEWARE + ["whitenoise.middleware.WhiteNoiseMiddleware"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
