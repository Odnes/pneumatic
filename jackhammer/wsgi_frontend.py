from .frontend_app import create_app
from dotenv import load_dotenv

# Done automatically on flask CLI / .run() method.
# Necessary for production servers.
# Path is relative to the working directory of the shell from which the python interpreter, be it of
# global or venv origin, is called.
load_dotenv(".flaskenv")

app = create_app()

# app.run(port=5002)
# use "flask run --port 5000" command in development. enable hot-reloading
