from admin_app import create_app


app = create_app()

app.run(port=5001)
# use "flask run --port 5000" command in development. enable hot-reloading
