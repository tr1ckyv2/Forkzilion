from userbot.modules.sql_helper import SESSION, BASE
from sqlalchemy import Column, String


class Gdrive(BASE):
    __tablename__ = "gdrive"
    user = Column(String(50), primary_key=True)

    def __init__(self, cat):
        self.user = user


Gdrive.__table__.create(checkfirst=True)


def is_folder(folder_id):
    try:
        return SESSION.query(Gdrive).filter(Gdrive.user == str(folder_id))
    except BaseException:
        return None
    finally:
        SESSION.close()


def gparent_id(folder_id):
    adder = SESSION.query(Gdrive).get(folder_id)
    if not adder:
        adder = Gdrive(folder_id)
    SESSION.add(adder)
    SESSION.commit()


def get_parent_id():
    try:
        return SESSION.query(Gdrive).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def rmparent_id(folder_id):
    note = SESSION.query(Gdrive).filter(Gdrive.user == folder_id)
    if note:
        note.delete()
        SESSION.commit()
