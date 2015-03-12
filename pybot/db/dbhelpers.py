from functools import partial
from pybot.db.dbmodel import (db, User, Page, 
                                Message, MessageType)

from sqlalchemy.orm.exc import NoResultFound

def add_to_db(obj: db.Model):
    db.session.add(obj)
    db.session.commit()

def remove_from_db(obj: db.Model):
   db.session.delete(obj)
   db.session.commit()

def create_user(*args, **kwargs):
    new_user = User(*args, **kwargs)
    add_to_db(new_user)

def get_user(userid=None, email=None, first_name=None, last_name=None):
    if userid:
        f = partial(User.query.filter_by, id=userid)
    elif email:
        f = partial(User.query.filter_by, email=email)
    elif first_name:
        f = partial(User.query.filter_by, first_name=first_name)
    elif last_name:
         f = partial(User.query.filter_by, last_name=last_name)

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

def create_page(title: str, content: str):
    new_page = Page(title, content)
    add_to_db(new_page)

def get_page(title: str):
    page = Page.query.filter_by(title=title).first()
    return page 

def change_page(title: str, **kwargs):
    page = get_page(title)
    if 'new_title' in kwargs:
        page.title = kwargs['new_title']
        del kwargs['new_title']
    for k, v in kwargs.items():
        page.__setattr__(k, v)
    db.session.commit()       

def delete_page(title: str):
    page = get_page(title)
    remove_from_db(page)


def get_header():
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

def get_footer():
    try:
        footer = Message.query.filter_by(
                            message_type=MessageType.footer).first()
    except NoResultFound:
        footer = None
    return footer

def set_footer(text: str):
    current_footer = get_footer()
    if current_footer:
        Message.query.filter_by(
                            message_type=MessageType.footer).update({Message.text: text})
        db.session.commit()
    else:
        new_footer = Message(MessageType.footer, text)
        add_to_db(new_footer)

