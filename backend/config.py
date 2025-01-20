import os


SECRET_KEY = os.getenv("SECRET_KEY", "chang-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1) # 1 minutes for testing
