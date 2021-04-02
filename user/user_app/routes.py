from flask import request, render_template, current_app, url_for, jsonify
from . import db
from .models import Tags, EpistemicStates, DocTypes, DocStatuses, Articles


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
                           paginated_articles=pagination.items,
                           next_url=next_url,
                           previous_url=previous_url,
                           title='jinja demo site',
                           description="smarter page templates \
                           with flask and jinja")


@current_app.route('/<doc_type>/<slug>')
def article_page(doc_type: str, slug: str):
    #  not sure if more efficient than just querying for slug
    #  at least guards for wrong doctype-slug combination in URL

    #  seems only one table may be filtered per filter, unless
    #  boolean operators are used, which defeats the purpose of
    #  filtering for type to save time (unlike logic operators, booleans
    #  need to ascertain right side truthiness).
    #  See comments:
    #  https://stackoverflow.com/a/41349608/11470799
    selected_article = Articles.query\
     .join(DocTypes).filter(DocTypes.name == doc_type)\
                    .filter(Articles.slug == slug).first()
    panagiotis = 5* doc_type

    return render_template('article_page.html', article=selected_article,
                           description="dedicated article page")


@current_app.route('/tag/<name>/')
def ssr_tag_page(name: str):
    page_number = request.args.get('page', 1, type=int)
    # for table-associated M2M relationships, join(ModelName) won't do
    # join(LeftModel.right_relationship) works though, making RightModel
    # accessible. Go figure!
    tagged_pagination = Articles.query\
                                .join(Articles.tags_list)\
                                .filter(Tags.name == name)\
                                .order_by(Articles.last_major_edit.desc())\
                                .paginate(page_number,
                                          current_app
                                          .config['ARTICLES_PER_PAGE'],
                                          True)
    #  url_for seemingly uses the decorator to build it's URLS, though
    #  it gets confusing when you put multiple route decorators
    #  also, arguments that don't belong to the URL (which one?) are
    #  placed as GET queries. lastly, if a function's route is dynamic, the
    #  URL variables need to be passed into url_for explicitly.

    #  ought to refactor, maybe dig into the url_for manual
    next_url = url_for('ssr_tag_page', name=name, page=tagged_pagination.next_num) \
        if tagged_pagination.has_next else None
    previous_url = url_for('ssr_tag_page', name=name, page=tagged_pagination.prev_num) \
        if tagged_pagination.has_prev else None

    return render_template('sample_page.html',
                           paginated_articles=tagged_pagination.items,
                           next_url=next_url,
                           previous_url=previous_url,
                           description="Semantically filtered page")


@current_app.route('/pull_semantics', methods=['POST'])
def pull_semantics():
    # request only has body field as payload, so no need to specify
    requested_slug = request.json
    article_for_slug = Articles.query.filter(
        Articles.slug == requested_slug).first()

    return jsonify(article_for_slug)
