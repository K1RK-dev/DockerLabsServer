from models.group import Group

def get_groups():
    try:
        groups = Group.query.all()
        if not groups:
            return None, "No groups found"
        return groups, None
    except Exception as e:
        return None, f"Error getting groups: {e}"