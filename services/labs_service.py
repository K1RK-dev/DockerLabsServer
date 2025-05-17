from extensions import db
from models.lab import Lab

def get_labs():
    try:
        labs = Lab.query.all()
        if not labs:
            return None, "No labs found"
        return labs, None
    except Exception as e:
        return None, f"Error getting labs: {e}"

def create_lab(title, description, image_id, user_id):
    try:
        new_lab = Lab(title=title, description=description, image_id=image_id, user_id=user_id)
        db.session.add(new_lab)
        db.session.commit()
    except Exception as e:
        return None, f"Error creating lab: {e}"
    return new_lab.id, None
