from resource import db


class Dictionary(db.Model):
    """词典表"""
    __tablename__ = "rs_analysis_event_library"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    file_name=db.Column(db.String(255))
    create_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Dictionary {}>'.format(self.name)