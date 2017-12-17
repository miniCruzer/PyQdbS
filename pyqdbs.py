import os
from PyQdbS import create_app

app = create_app(os.environ.get("PYQDBS_CONFIG", "ProductionConfig"))

if __name__ == '__main__':
	app.run()
