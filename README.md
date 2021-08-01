# jackhammer
It's a minimal website revision system (CMS, if you must) built with flask.

# Features
- Tufte-CSS sidenotes
- Renders from sqlite, creates/updates through markdown files extended with metadata and sidenote syntax.
- Highlights presently displayed article, draws corresponding metadata on the fly.
- Usable without JavaScript.
yada yada and to be continued.

# Installation
1. Clone the repo.
2. Start and activate a python venv, do `pip install -r requirements.txt`.
3. Add environment variables to PARENT/.flaskenv (edit secret key, db path appropriately) like so:
  ```
  FLASK_ENV=production
  SECRET_KEY=changemeplz
  SQLALCHEMY_DATABASE_URI=sqlite:////path/to/file.db
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  ```
4. Uncomment `db.create_all()` in the `__init__.py` of the admin app for the first run, in order to create the db schema.
5. Run with a wsgi compatible server (e.g. gunicorn).
6. Structure your  `article_template.md` for your articles, put them on an "articles" folder on the same level as the cloned repo.
7. Use `DOMAIN_ROOT/article_from_md?filename=example.md` to create your first article.
8. Use the routes of the admin app to add missing metadata. Tags are added automatically.
9. *(recommended)* Reverse proxy the frontend app through nginx, run admin app locally w/ VPN (e.g. wireguard) access for site admins.
