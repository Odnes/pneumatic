from os import environ
import re


class Config:
    # Articles repository
    def __init__(self):
        # Target the raw text files in case a github repository is provided.
        self.ARTICLES_REPO = environ.get("articles_repo")

        is_github = re.match(
                      r".*github.com\/(\w+)\/(\w+)($|\.git$|\/tree/(\w+)$)",
                      self.ARTICLES_REPO)
        if is_github:
            repo_details = is_github.groups()
            # user, repository name, branch, respectively
            self.ARTICLES_REPO = r"https://raw.githubusercontent.com/" +\
                repo_details[0] + "/" + repo_details[1] +\
                "/blob/" + repo_details[3]

    # General
    secret_key = environ.get('secret_key')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = \
        environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    ARTICLES_PER_PAGE = 3

