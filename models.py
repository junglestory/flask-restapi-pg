from sqlalchemy import Column, String, Integer, TEXT, DATETIME
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Board(db.Model):
    __tablename__ = "board"

    board_no = db.Column(Integer, primary_key=True, index=True)
    title = db.Column(String(200))
    contents = db.Column(TEXT)
    writer = db.Column(String(50))
    view_count = db.Column(Integer)
    link_url = db.Column(String(200))
    create_date = db.Column(DATETIME(timezone=True), server_default=func.now())
    update_date = db.Column(DATETIME(timezone=True), server_default=func.now())

    def __init__(self, title, contents, writer, view_count, link_url):
        self.title = title
        self.contents = contents
        self.writer = writer
        self.view_count = view_count
        self.link_url = link_url


    def to_json(self):
        return {
            'board_no': self.board_no,
            'title': self.title,
            'contents': self.contents,
            'writer': self.writer,
            'view_count': self.view_count,
            'link_url': self.link_url,
            'create_date': self.create_date,
            'update_date': self.update_date
        }