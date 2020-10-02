from . import db
from dataclasses import dataclass
from datetime import date

# Docs: flask-sqlalchemy "Declaring Models", sqlalchemy "Basic Relationship
# Patterns"

# intermediary tables for M2M associations should not be declared as classes,
# unless they are intended to contain additional columns (i.e. columns that
# are not foreign keys to the left and right tables). For the last scenario,
# look up "Association object".
article_tags = db.Table('article_tags',
                        db.Column('article_id', db.Integer,
                                  db.ForeignKey('articles.id'),
                                  primary_key=True),
                        db.Column('tag_id', db.Integer,
                                  db.ForeignKey('tags.id'),
                                  primary_key=True)
                        )


@dataclass
class Tags(db.Model):
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40),
                     unique=True,
                     index=True,
                     nullable=False)
    category = db.Column(db.Integer)


@dataclass
class EpistemicStates(db.Model):
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,
                     unique=True,
                     nullable=False)


@dataclass
class DocTypes(db.Model):
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,
                     unique=True,
                     nullable=False)


@dataclass
class DocStatuses(db.Model):
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,
                     unique=True,
                     nullable=False)


@dataclass
class Articles(db.Model):
    # Dataclass JSON serialisation doesn't return dynamic fields
    # Ignoring unneeded fields.
    importance: int
    last_major_edit: date
    tags_list: Tags
    epistemic_state: EpistemicStates
    doc_type: DocTypes
    status: DocStatuses

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100),
                     unique=True,
                     nullable=False)
    title = db.Column(db.String(140),
                      unique=True,
                      index=True,
                      nullable=False)
    content = db.Column(db.Text, nullable=False)
    importance = db.Column(db.Integer, nullable=False)
    last_major_edit = db.Column(db.Date, index=True, nullable=False)
    epistemic_state_id = db.Column(db.Integer,
                                   db.ForeignKey('epistemic_states.id'),
                                   nullable=False)
    type_id = db.Column(db.Integer,
                        db.ForeignKey('doc_types.id'),
                        nullable=False
                        )
    status_id = db.Column(db.Integer,
                          db.ForeignKey('doc_statuses.id'),
                          nullable=False
                          )

# relationship() is like foreign key mapping but for orm classes, beats me
# why this isn't done implicitly by default. backref defines the inverse
# relationship property at the related class. Can be done manually using the
# back_populates option of relationship() on both classes.

# not sure about lazy values, just pasted them from similar
# scenario in flask docs.
    tags_list = db.relationship('Tags', secondary=article_tags,
                                lazy='subquery',
                                backref=db.backref('article_list', lazy=True)
                                )
    epistemic_state = db.relationship("EpistemicStates",
                                      backref='article_list'
                                      )
# Risky to use "type" as variable name
    doc_type = db.relationship('DocTypes', backref='article_list')
    status = db.relationship("DocStatuses", backref='article_list')

    def __repr__(self):
        return 'Article titled: \'{}\''.format(self.title)
