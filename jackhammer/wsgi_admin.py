from .admin_app import create_app
from dotenv import load_dotenv

# Done automatically on flask CLI / .run() method.
# Necessary for production servers.
load_dotenv(".flaskenv")

app = create_app()

# app.run(port=5001)
# use "flask run --port 5000" command in development. enable hot-reloading
