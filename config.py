class PybotConfig:
	pass

class DebugConfig(PybotConfig):
	'SQLALCHEMY_DATABASE_URI' = 'sqlite:////tmp/test.db'

class ProductionConfig(PybotConfig):
	'SQLALCHEMY_DATABASE_URI' = 'sqlite:////pybot.db'