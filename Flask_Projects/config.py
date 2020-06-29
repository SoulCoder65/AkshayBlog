import os

from dotenv import load_dotenv
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
	#SETTING SECURITY KEY
	SECRET_KEY=os.getenv("SECRETKEY")

	# SETTING SQLAlchemy
	SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE")

	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME =os.getenv("EMAIL")
	
	
	MAIL_PASSWORD =os.getenv("EMAIL_PASS")