from resource import db

class TextLibrary(db.Model):
    """文本库表"""
    __tablename__ = "rs_textlibrary"
    id = db.Column(db.Integer,primary_key=True)
    textlibrary_name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    line_no = db.Column(db.Integer)
    create_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)


    def __repr__(self):
        return '<TEXT_LIBRARY {}>'.format(self.textlibrary_name)