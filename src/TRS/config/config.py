from constants import DB_USER, DB_PWD, DB_HOST, DB_NAME

class DevelopmentConfig:
  INIT_DB = False

  # submission path
  SUB_PATH = None

  # SQLALCHEMY
  SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}'
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  SQLALCHEMY_ENGINE_OPTIONS = {
      'isolation_level': "AUTOCOMMIT"
  }

  # Seed data
  SEED_QUESTION_LEVEL = False
