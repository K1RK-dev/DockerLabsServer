import os
from docker.errors import APIError, NotFound, BuildError
from app import Config
from models import Dockerfile, Image, Container
from extensions import db
from docker import from_env


def create_dockerfile(file):
    filename = 'Dockerfile_' + file.filename
    file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
    new_dockerfile = Dockerfile(filename=filename)
    new_dockerfile.set_filename(filename)
    new_dockerfile.set_path(Config.UPLOAD_FOLDER + filename)
    db.session.add(new_dockerfile)
    db.session.commit()
    return new_dockerfile, None


def delete_dockerfile(dockerfile):
    if Image.query.filter_by(dockerfile_id=dockerfile.id):
        return None, "Cannot delete Dockerfile while its attached to the image"
    if not os.path.isfile(Config.UPLOAD_FOLDER + dockerfile.filename):
        return None, "File not found"
    try:
        os.remove(Config.UPLOAD_FOLDER + dockerfile.filename)
        dockerfile.delete()
        return dockerfile.id, None
    except Exception as e:
        return None, f"Cannot remove file {dockerfile.filename}: {e}"

def get_images(user_id = 0):
    if user_id == 0:
        images = Image.query.all()
        if not images:
            return [], f"No images found"
        return images, None
    else:
        images = Image.query.filter_by(user_id=user_id).all()
        if not images:
            return [], f"No images found"
        return images, None

def create_image(name, dockerfile_id, user_id):
    new_image = Image(name=name, dockerfile_id=dockerfile_id, user_id=user_id)
    db.session.add(new_image)
    db.session.commit()
    return new_image, None


def build_image(image):
    try:
        client = from_env()
        dockerfile = Config.UPLOAD_FOLDER + image.dockerfile.filename
        if not os.path.isfile(dockerfile):
            return None, f"Dockerfile not found: {dockerfile}"

        with open(dockerfile, 'rb') as f:
            try:
                response = client.api.build(fileobj=f, tag=image.name, decode=True)
                image_id = None
                for line in response:
                    if 'stream' in line:
                        print(line['stream'], end='')
                    elif 'error' in line:
                        return None, f"Error building image: {line['error']}"
                    elif 'aux' in line and 'ID' in line['aux']:
                        image_id = line['aux']['ID']

                if image_id:
                    image.image_id = image_id
                    db.session.add(image)
                    db.session.commit()
                    return image, None
                else:
                    return None, "Image ID not found in build logs."

            except BuildError as e:
                return None, f"Error building image: {e.msg}\n{e.build_log}"
            except APIError as e:
                return None, f"Error building image: {e}"
    except NotFound as e:
        return None, f"Dockerfile not found: {e}"
    except APIError as e:
        return None, f"Error building image: {e}"
    except Exception as e:
        return None, str(e)


def delete_image(image):
    try:
        if image.image_id:
            client = from_env()
            client.images.remove(image.image_id)
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
    return container.id, None


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
        container = client.containers.run(image.name, detach=True, ports={'8000/tcp': None})
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
    return container.id, None
