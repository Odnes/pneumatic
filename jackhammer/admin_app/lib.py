import markdown
import datetime
import re
import string
import requests
from flask import current_app
from ..models import Tags, DocTypes, DocStatuses


def read_file(filename, repo_url=current_app.config['ARTICLES_REPO']):
    print("Attempting to access remote file: " + f'{repo_url}/{filename}')
    text = requests.get(f'{repo_url}/{filename}').text
    return text


# Is meant for unique db keys.
def db_id_for_meta_value(meta_value, db_object):
    existing = db_object.query.filter(db_object.name ==
                                      meta_value
                                      ).first()
# try/catch
    if existing is None:
        return 'Value \'' + meta_value + '\' not in database. Aborting.'

    print('Retrieved id for: ' + meta_value)
    return existing.id


def convert_sidenotes(source_text):
    def unique_id_replacement(match_obj):
        # mended .md is returned after unique_id_replacement() runs
        # count times (optional argument in .sub() )
        dirty_slug = "-".join(match_obj.group(1)
                              .split(sep=" ", maxsplit=6)[:5]).lower()
        clean_slug = dirty_slug.translate(str.maketrans('', '',
                                          string.punctuation.replace('-', '')))
        sidenote_html = \
            f"""
                <label for="sn-{clean_slug}">⊕</label>
                <input  type="checkbox" class="note-toggle"
                id="sn-{clean_slug}" >
                <sup class="sidenote">{match_obj.group(1)}</sup>
             """
        return sidenote_html
    # Is a RegEx solution the simplest possible?
    pattern = re.compile(r'\n\* (.*) \*\n')
    md_with_sidenotes = pattern.sub(unique_id_replacement, source_text)
    return md_with_sidenotes


def dict_from_md(filename):
    REQUIRED_META = {'slug', 'title', 'last_major_edit',
                     'type', 'status'}
    OPTIONAL_META = {'tags_list'}
    source_text = read_file(filename)

    md_with_sidenotes = convert_sidenotes(source_text)

    md = markdown.Markdown(extensions=['meta'])
#  There's also convertFile, but it only outputs to files or stdout, so I went
#  manual
    html = md.convert(md_with_sidenotes)
    metadata = md.Meta
    tags = []
    prepared_dict = {}
# try/catch
# {*dict} fetches set of keys in dict. Weird but concise. Just get used to it.
    if(not ({*metadata} == REQUIRED_META or
       {*metadata} == REQUIRED_META | OPTIONAL_META)):
        return "Missing or malformed .md file (use article_template.md)"

    if 'tags_list' in metadata:
        tags_in_file = metadata.pop('tags_list')
        for name in tags_in_file:
            existing_in_db = Tags.query.filter(Tags.name == name).first()
            if existing_in_db:
                print('Tag \'' + name + '\' already exists.')
                tags.append(existing_in_db)
            else:
                # Unrecognized tags are automatically saved as domain tags.
                tags.append(Tags(name=name, category=1))
                # Should be printed in html response instead.
                print('New domain tag \'' + name + '\' to be created.')
        print('Tags to be appended: ')
        for i in tags:
            print(i.name + ', ')

    prepared_dict['content'] = html
# Named 'tags_list' to mirror attribute of 'Articles' orm class
    prepared_dict['tags_list'] = tags
    for key in metadata:
        prepared_dict[key] = ''.join(metadata[key])
# convert date string to 'date' object
    prepared_dict['last_major_edit'] =\
        datetime.datetime.strptime(prepared_dict['last_major_edit'],
                                   "%d/%m/%Y").date()

# no guard for function fail (e.g. nonexistent key)
    type_id = db_id_for_meta_value(prepared_dict['type'], DocTypes)
    status_id = db_id_for_meta_value(prepared_dict['status'], DocStatuses)

    del prepared_dict['type']
    prepared_dict['type_id'] = type_id
    del prepared_dict['status']
    prepared_dict['status_id'] = status_id

    return prepared_dict
