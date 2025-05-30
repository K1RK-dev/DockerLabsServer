from extensions import db

class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    container_id = db.Column(db.String(255), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=True)
    lab = db.relationship('Lab', backref='container', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref='container', lazy=True)

    def __repr__(self):
        return f'<Container {self.container_id}>'