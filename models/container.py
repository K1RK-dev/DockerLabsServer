from extensions import db

class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    container_id = db.Column(db.String(255), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=True)
    lab = db.relationship('Lab', backref='container', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref='container', lazy=True)

    @staticmethod
    def get_by_id(container_id):
        container = Container.query.filter_by(container_id=container_id).first()
        if container:
            return container
        else:
            return None

    def __repr__(self):
        return f'<Container {self.container_id}>'
