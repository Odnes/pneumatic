from os import environ
import re


class Config:
    # Articles repository URL
    ARTICLES_REPO = environ.get("ARTICLES_REPO")

    # General
    SECRET_KEY = environ.get('SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = \
        environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    ARTICLES_PER_PAGE = 3

    def __init__(self):
        # For ARTICLES_REPO, target the raw text files in case a github
        # repository is provided.
        is_github = re.match(
                      r".*github.com\/(\w+)\/(\w+)($|\.git$|\/tree/(\w+)$)",
                      self.ARTICLES_REPO)
        if is_github:
            repo_details = is_github.groups()
            # user, repository name, branch (optional), respectively
            textfiles_url = r"https://raw.githubusercontent.com/" +\
                repo_details[0] + "/" + repo_details[1] +\
                "/blob/"
            if repo_details[3]:
                textfiles_url+= repo_details[3]
            
            self.ARTICLES_REPO = textfiles_url


# Instantiate the class, so that I may customize the ARTICLES_REPO attribute
# through the constructor (though app.config.from_object() can target 
# uninstantiated class objects as well).
default_config = Config()
