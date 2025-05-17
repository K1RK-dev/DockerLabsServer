from extensions import db

class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    image = db.relationship('Image', backref='lab', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='lab', lazy=True)

    def __repr__(self):
        return f'<Lab {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image.to_dict() if self.image else None,
            'user': self.user.to_dict() if self.user else None,
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()