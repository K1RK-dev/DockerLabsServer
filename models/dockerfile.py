from extensions import db

class Dockerfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref='dockerfile', lazy=True)

    def set_filename(self, filename):
        self.filename = filename

    def set_user_id(self, user_id):
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'user_id': self.user_id,
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Image {self.filename}>'