from flask import request, current_app
from . import db
from models import Tags, DocTypes, DocStatuses, Articles
from .lib import dict_from_md


@current_app.route('/admin')
def hello():
    return "Admin welcome page"

@current_app.route('/admin/create_tag')
def create_tag():
    name = request.args.get('name')
    category = request.args.get('category')
    if name and category:
        existing_tag = Tags.query.filter(Tags.name == name).first()
        if existing_tag:
            return f'{name} already created!'
        new_tag = Tags(name=name, category=category)
        db.session.add(new_tag)
        db.session.commit()
    return f'{new_tag} succesfully created'

# needs DRYing up via metaprogramming
@current_app.route('/admin/create_status')
def create_status():
    name = request.args.get('name')
    if name:
        existing_statuses = DocStatuses.query.filter(DocStatuses.name ==
                                                 name).first()
        if existing_statuses:
            return f'{name} already created!'
        new_status = DocStatuses(name=name)
        db.session.add(new_status)
        db.session.commit()
    return f"Status '{new_status}' succesfully created"


@current_app.route('/admin/create_type')
def create_type():
    name = request.args.get('name')
    if name:
        existing_types = DocTypes.query.filter(DocTypes.name ==
                                                 name).first()
        if existing_types:
            return f"Type '{name}' already created!"
        new_type = DocTypes(name=name)
        db.session.add(new_type)
        db.session.commit()
    return f'{new_type} succesfully created'


@current_app.route('/admin/article_from_md')
def article_from_md(**kwargs):
    # called from update_article with dict already prepared
    if 'dict' in kwargs:
        prepared_dict = kwargs['dict']
    else:
        filename = request.args.get('filename', None, type=str)
        prepared_dict = dict_from_md(filename)
        #  Alternate output is error string; should use try/catch instead
        if not isinstance(prepared_dict, dict):
            return 'Failed converting md file to dictionary. <br>' +\
                    prepared_dict

    existing_slug = Articles.query.filter(Articles.slug ==
                                          prepared_dict['slug']
                                          ).first()
    existing_title = Articles.query.filter(Articles.title ==
                                           prepared_dict['title']
                                           ).first()
#  try/catch
    if existing_title or existing_slug:
        return 'Title/slug already exists. Aborting.'

    new_article = Articles(**prepared_dict)
# it does not matter at which point an object is added to the session,
# provided it's done prior to commitment. All relationship() bound
# objects will also be added and commited, provided they exist.
    db.session.add(new_article)
    db.session.commit()
    return f'{new_article} succesfully commited from markdown'


@current_app.route('/admin/update_article')
def update_article():
    filename = request.args.get('filename', None, type=str)
    prepared_dict = dict_from_md(filename)
#  try/catch
    if not isinstance(prepared_dict, dict):
        return 'Failed converting md file to dictionary. Update aborted.'

    if 'slug' not in prepared_dict or 'title' not in prepared_dict:
        return 'Missing title/slug. Update aborted.'
# DB object is matched with 'slug'. Title update is allowed, but
# discouraged, since uniqueness is not programmatically assured.
# (dbms should handle it though)
    article_to_update = Articles.query.filter(Articles.slug ==
                                              prepared_dict['slug']
                                              ).first()
    if article_to_update is None:
        return 'No matching article in database. Update aborted.'

    db.session.delete(article_to_update)
    return article_from_md(dict=prepared_dict)+'<br>Update operation returned.'
