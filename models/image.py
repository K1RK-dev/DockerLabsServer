from extensions import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    image_id = db.Column(db.String(255), nullable=True)
    dockerfile_id = db.Column(db.Integer, db.ForeignKey('dockerfile.id'), nullable=False)
    dockerfile = db.relationship('Dockerfile', backref='images', lazy=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    teacher = db.relationship('User', backref='image', lazy=True)

    def __repr__(self):
        return f'<Image {self.name}>'