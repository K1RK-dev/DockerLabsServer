from extensions import db

class Dockerfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    teacher = db.relationship('User', backref='dockerfile', lazy=True)

    def set_filename(self, filename):
        self.filename = filename

    def set_teacher_id(self, teacher_id):
        self.teacher_id = teacher_id

    def __repr__(self):
        return f'<Image {self.filename}>'