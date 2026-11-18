import os

URI = os.environ.get("DATABASE_URL") or "mysql+pymysql://root:@127.0.0.1:3306/portfolio"

if URI.startswith("mysql://"):
    URI = URI.replace("mysql://", "mysql+pymysql://", 1)

SECRET_KEY = os.environ.get("SECRET_KEY") or "clave-solo-para-desarrollo"
