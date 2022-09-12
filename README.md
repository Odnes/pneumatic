# pneumatic
A minimal website revision system (CMS, if you must) built with flask. [Live instance](https://tiptheiceberg.com)

## Features
- Tufte-CSS sidenotes
- Renders from sqlite, creates/updates through markdown files extended with metadata and sidenote syntax.
- Highlights presently displayed article, draws corresponding metadata on the fly.
- Usable without JavaScript.
yada yada and to be continued.

## Installation
1. Clone the repo.
2. Start and activate a python venv in the repo's root folder, do `pip install -r requirements.txt`.
3. Add environment variables to $REPO_ROOT/.flaskenv, see template.flaskenv. 
4. Structure your articles after `article_template.md`, place them on the web location pointed to by `ARTICLES_REPO`. If it points to a github repo, you're good to go. Otherwise, you also have to provide an ARTICLES_INDEX url that returns a json list of articles with a name field pointing to each file.
5. Throw in a metadata_manifest.csv file with each row containing the values for
   each metadata property. Currently, 'type' and 'status' properties are supported (in
   that order). Make sure every value assigned to your articles is listed here.
   Otherwise, processing of the respective articles will fail. Don't worry about
   tags, they are added automatically.
6. Use the /generate_db admin endpoint and you're set.
7. Run with a wsgi compatible server (e.g. gunicorn).
9. *(recommended)* Reverse proxy the frontend app through nginx, run admin app locally w/ VPN (e.g. wireguard) access for site admins.
