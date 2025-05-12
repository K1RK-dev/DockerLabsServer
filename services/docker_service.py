from os.path import join, exists
from docker.errors import APIError, NotFound
from app import Config
from models import Dockerfile, Image, Container, dockerfile
from extensions import db
from docker import from_env


def create_dockerfile(file):
    filename = 'Dockerfile_' + file.filename
    file.save(join(Config.UPLOAD_FOLDER, filename))
    new_dockerfile = Dockerfile(filename=filename)
    new_dockerfile.set_filename(filename)
    new_dockerfile.set_path(Config.UPLOAD_FOLDER + filename)
    db.session.add(new_dockerfile)
    db.session.commit()
    return new_dockerfile, None

def create_image(name, dockerfile_id, teacher_id):
    new_image = Image(name=name, dockerfile_id=dockerfile_id, teacher_id=teacher_id)
    db.session.add(new_image)
    db.session.commit()
    return new_image, None

def build_image(image):
    try:
        client = from_env()
        dockerfile = Config.UPLOAD_FOLDER + image.dockerfile.filename
        if not exists(dockerfile):
            return None, f"Dockerfile not found: {dockerfile}"
        with open(dockerfile, 'rb') as f:
            try:
                image, build_log = client.images.build(fileobj=f, tag=image.name)
            except APIError as e:
                return None, f"Error building image: {e}"
            f.close()
    except NotFound as e:
        return None, f"Dockerfile not found: {e}"
    except APIError as e:
        return None, f"Error building image: {e}"
    except Exception as e:
        return None, str(e)
    return image, None

def delete_image(image):
    try:
        client = from_env()
        client.images.remove(image.id)
        db.session.delete(image)
        db.session.commit()
        return image, None
    except NotFound as e:
        return None, f"Image not found: {e}"
    except APIError as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)

def start_container(container):
    try:
        client = from_env()
        container = client.containers.get(container.container_id)
        container.start()
    except NotFound as e:
        return None, f"Container not found: {e}"
    except APIError as e:
        return None, f"Error starting container: {e}"
    except Exception as e:
        return None, str(e)
    return None, None

def stop_container(container):
    try:
        client = from_env()
        container = client.containers.get(container.container_id)
        container.stop()
    except NotFound as e:
        return None, f"Container not found: {e}"
    except APIError as e:
        return None, f"Error stopping container: {e}"
    except Exception as e:
        return None, str(e)
    return None, None

def run_container(image):
    try:
        client = from_env()
        container = client.containers.run(image.name, detach=True)
        container_model = Container()
        container_model.container_id = container.id
        container_model.name = container.name
        db.session.add(container_model)
        db.session.commit()
    except NotFound as e:
        return None, f"Image not found: {e}"
    except APIError as e:
        return None, f"Error running container: {e}"
    except Exception as e:
        return None, str(e)
    return container, None
