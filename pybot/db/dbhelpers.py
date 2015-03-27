import pybot.helpers

from functools import partial
from pybot.db.dbmodel import (db, User, Page, Category, 
                                Message, MessageType,
                                Link)

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import mistune

def add_to_db(obj: db.Model) -> bool:
    db.session.add(obj)
    try:
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False

def remove_from_db(obj: db.Model):
   db.session.delete(obj)
   db.session.commit()

# users

def create_user(email=None, first_name=None, last_name=None, password=None) -> bool:
    new_user = User(email, first_name, last_name)
    new_user.password = password
    return add_to_db(new_user)

def get_user(userid=None, email=None, first_name=None, last_name=None) -> User:
    if userid:
        f = partial(User.query.filter_by, id=userid)
    elif email:
        f = partial(User.query.filter_by, email=email)
    elif first_name:
        f = partial(User.query.filter_by, first_name=first_name)
    elif last_name:
         f = partial(User.query.filter_by, last_name=last_name)
    else:
        return None

    return f().first()

def change_user(email: str, **kwargs):
    user = get_user(email=email)
    if 'new_email' in kwargs:
        user.email = kwargs['new_email']
        del kwargs['new_email']
    for k, v in kwargs.items():
        user.__setattr__(k, v)
    db.session.commit()

def delete_user(email: str):
    user = get_user(email=email)
    remove_from_db(user)

# pages 

def get_page_slugs():
    for page in Page.query.all():
        yield page.slug

def create_page(title: str, content_markdown: str, category_title='Main'):
    content_html = mistune.markdown(content_markdown)
    slug = pybot.helpers.slugify(title)
    category = get_page_category(title=category_title)
    if not category:
        category = create_category(category_title)
    new_page = Page(title, slug, content_markdown, content_html, category)
    if add_to_db(new_page):
        return {'title': title, 'slug': slug}
    else:
        return None

def get_page(slug: str, title: str) -> Page:
    query = {'slug': slug} if slug else {'title': title}
    try:
        page = Page.query.filter_by(**{query}).first()
    except NoResultFound:
        page = None
    return page

def get_all_pages() -> [Page]:
    return Page.query.all()

def modify_page(slug: str, **kwargs):
    page = get_page(slug)
    if 'new_title' in kwargs:
        page.slug = kwargs['new_title']
        del kwargs['new_title']
    for k, v in kwargs.items():
        page.__setattr__(k, v)
    db.session.commit()       

def delete_page(slug: str):
    page = get_page(slug)
    remove_from_db(page)

# page categories

def create_category(title: str):
    slug = pybot.helpers.slugify(title)
    new_category = Category(title, slug)
    if add_to_db(new_category):
        return {'title': title, 'slug': slug}
    else:
        return None

def get_page_category(slug=None, title=None):
    query = {'slug': slug} if slug else {'title': title}
    try:
        return Category.query.filter_by(**{query}).first()
    except NoResultFound:
        return None

def get_all_page_categories() -> [Category]:
    return Category.query.all()

# header

def get_header() -> Message:
    try:
        header = Message.query.filter_by(
            message_type=MessageType.header).first()
    except NoResultFound:
        header = None
    return header

def set_header(text: str):
    current_header = get_header()
    if current_header:
        Message.query.filter_by(
                            message_type=MessageType.header).update({Message.text: text})
        db.session.commit()
    else:
        new_header = Message(MessageType.header, text)
        add_to_db(new_header)

# footer

def get_footer() -> Message:
    try:
        footer = Message.query.filter_by(
                            message_type=MessageType.footer).first()
    except NoResultFound:
        footer = None
    return footer

def set_footer(text: str) -> bool:
    current_footer = get_footer()
    if current_footer:
        Message.query.filter_by(
                            message_type=MessageType.footer).update({Message.text: text})
        db.session.commit()
    else:
        new_footer = Message(MessageType.footer, text)
        return add_to_db(new_footer)

# links

def add_link(text: str, endpoint='', variable='') -> bool:
    new_link = Link(text, endpoint, variable)
    return add_to_db(new_link)

def get_links() -> [Link]:
    try:
        return Link.query.all()
    except Exception: # change to the actual exception
        return []

def remove_link(text: str) -> bool:
    try:
        link = Link.query.filter_by(text=text).first()
    except NoResultFound:
        return False
    remove_from_db(link)
    return True

