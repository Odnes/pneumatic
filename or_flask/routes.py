from flask import request, render_template
from flask import current_app
from .models import db, Tags


@current_app.route('/')
def hello():
    nav = Tags.query.all()
    return render_template('sample_page.html', nav=nav,
                           title='jinja demo site',
                           description="smarter page templates \
                           with flask and jinja")


@current_app.route('/create_tag')
def create_user():
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
