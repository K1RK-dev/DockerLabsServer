from extensions import db

class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    image = db.relationship('Image', backref='lab', lazy=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher = db.relationship('User', backref='lab', lazy=True)

    def __repr__(self):
        return f'<Lab {self.title}>'