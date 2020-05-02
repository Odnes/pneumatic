from flask import request, render_template, current_app, url_for
from . import db
from .models import Tags, EpistemicStates, DocTypes, DocStatuses, Articles
from .lib import dict_from_md


@current_app.route('/')
def hello():
    page_number = request.args.get('page', 1, type=int)
    tags_nav = Tags.query.all()
    epistemic = EpistemicStates.query.all()
    types = DocTypes.query.all()
    status = DocStatuses.query.all()
    pagination = Articles.query.order_by(Articles.last_major_edit.desc())\
        .paginate(page_number, current_app.config['ARTICLES_PER_PAGE'], True)
    next_url = url_for('hello', page=pagination.next_num) \
        if pagination.has_next else None
    previous_url = url_for('hello', page=pagination.prev_num) \
        if pagination.has_prev else None
    return render_template('sample_page.html', tags_nav=tags_nav,
                           epistemic=epistemic,
                           types=types,
                           status=status,
                           article=pagination.items,
                           next_url=next_url,
                           previous_url=previous_url,
                           title='jinja demo site',
                           description="smarter page templates \
                           with flask and jinja")


@current_app.route('/create_tag')
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


@current_app.route('/create_meta')
def create_meta():
    name = request.args.get('name')
    if name:
        existing_meta = DocStatuses.query.filter(DocStatuses.name ==
                                                 name).first()
        if existing_meta:
            return f'{name} already created!'
        new_meta = DocStatuses(name=name)
        db.session.add(new_meta)
        db.session.commit()
    return f'{new_meta} succesfully created'


@current_app.route('/article_from_md')
def article_from_md(**kwargs):
    # called from update_article with dict already prepared
    if 'dict' in kwargs:
        prepared_dict = kwargs['dict']
    else:
        filename = request.args.get('filename', None, type=str)
        prepared_dict = dict_from_md(filename)
        #  try/catch
        if not isinstance(prepared_dict, dict):
            return 'Failed converting md file to dictionary.'

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


@current_app.route('/update_article')
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
