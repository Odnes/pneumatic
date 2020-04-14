from flask import request, render_template
from flask import current_app
from .models import db, Tags, EpistemicStates, DocTypes, DocStatuses, Articles
import markdown
import datetime


@current_app.route('/')
def hello():
    nav = Tags.query.all()
    epistemic = EpistemicStates.query.all()
    types = DocTypes.query.all()
    status = DocStatuses.query.all()
    article = Articles.query.all()
    return render_template('sample_page.html', nav=nav,
                           epistemic=epistemic,
                           types=types,
                           status=status,
                           article=article,
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
def article_from_md():
    with open('sample_article.md', 'r') as file:
        text = file.read()
    md = markdown.Markdown(extensions=['meta'])
#  There's also convertFile, but it only outputs to files or stdout, so I went
#  manual
    html = md.convert(text)
    tags_list = []
    prepare_dict = md.Meta

    if ('slug' in prepare_dict and
        'title' in prepare_dict and
        'importance' in prepare_dict and
        'last_major_edit' in prepare_dict and
        'epistemic_state' in prepare_dict and
        'type' in prepare_dict and
            'status' in prepare_dict):

        if 'tags_list' in prepare_dict:
            tags = prepare_dict.pop('tags_list')
            for name in tags:
                existing = Tags.query.filter(Tags.name == name).first()
                if existing:
                    print('Tag \'' + name + '\' already exists.')
                    tags_list.append(existing)
                else:
                    tags_list.append(Tags(name=name, category=1))
                    print('New domain tag \'' + name + '\' created.')
            print('Tags to be appended: ')
            for i in tags_list:
                print(i.name + ', ')

        for key in prepare_dict:
            prepare_dict[key] = ''.join(prepare_dict[key])
        prepare_dict['content'] = html
        prepare_dict['tags_list'] = tags_list
        prepare_dict['last_major_edit'] =\
            datetime.datetime.strptime(prepare_dict['last_major_edit'],
                                       "%d/%m/%Y").date()

        existing_slug = Articles.query.filter(Articles.slug ==
                                              prepare_dict['slug']
                                              ).first()
        existing_title = Articles.query.filter(Articles.title ==
                                               prepare_dict['title']
                                               ).first()
        if existing_title or existing_slug:
            return 'Title/slug already exists. Aborting.'
            exit()

        def findDbIdForValue(key, db_object):
            existing = db_object.query.filter(db_object.name ==
                                              prepare_dict[key]
                                              ).first()
            if existing is None:
                print('Value ' + key + ': ' + prepare_dict[key] +
                      ' not existing. Aborting.')
                exit()
            else:
                print('All good for' + key)
                return existing.id

        es_id = findDbIdForValue('epistemic_state', EpistemicStates)
        type_id = findDbIdForValue('type', DocTypes)
        status_id = findDbIdForValue('status', DocStatuses)

        del prepare_dict['epistemic_state']
        prepare_dict['epistemic_state_id'] = es_id
        del prepare_dict['type']
        prepare_dict['type_id'] = type_id
        del prepare_dict['status']
        prepare_dict['status_id'] = status_id

        new_article = Articles(**prepare_dict)
# it does not matter at which point an object is added to the session,
# provided it's done prior to commitment. All relationship() bound
# objects will also be added and commited, provided they exist.
        db.session.add(new_article)
        db.session.commit()
        return f'{new_article} succesfully commited from markdown'
    else:
        return 'Missing required metadata keys'
