import docker
import select

from flask_login import login_required

docker_client = docker.from_env()

def register_socketio_handlers(socketio):
    @socketio.on('connect')
    def test_connect():
        print("Connected")
        socketio.emit('message', {'data': 'Connected'})

    @socketio.on('disconnect')
    def test_disconnect():
        print("Disconnected")
        socketio.emit('message', {'data': 'Disconnected'})

    @socketio.on('start_shell')
    @login_required
    def start_shell(container_id):
        try:
            container = docker_client.containers.get(container_id)
            if container.status != 'running':
                socketio.emit('terminal_output', {'output': f"Container {container_id} not running"}, 'error')
                return
            cmd = ['/bin/bash']
            socketio.start_background_task(target=shell_process, container=container, cmd=cmd)
        except docker.errors.NotFound:
            socketio.emit('terminal_output', {'output': f"Container {container_id} not found."})
        except Exception as e:
            socketio.emit('terminal_output', {'output': f"Error starting shell: {str(e)}"})

    def shell_process(container, cmd):
        try:
            exec_result = container.exec_run(cmd, stream=True, tty=True, socket=True)
            socket = exec_result.socket
            socket.setblocking(False)

            while True:
                read_sockets, _, _ = select.select([socket], [], [], 1)  # Timeout of 1 second
                if read_sockets:
                    try:
                        data = socket.recv(4096)
                        if not data:
                            break

                        output = data.decode('utf-8', errors='ignore')
                        socketio.emit('terminal_output', {'output': output})

                    except socket.timeout:
                        pass
                    except Exception as e:
                        print(f"Error receiving data: {e}")
                        break
                else:
                    pass

            socket.close()
            print("Shell process finished")

        except Exception as e:
            print(f"Error in shell process: {e}")
            socketio.emit('terminal_output', {'output': f"Error in shell process: {str(e)}"})

    @socketio.on('terminal_input')
    def terminal_input(data):
        container_id = data['container_id']
        input_data = data['input']
        try:
            container = docker_client.containers.get(container_id)
            exec_instance = container.exec_run(['/bin/bash', '-c', input_data], stream=False, tty=False)

            output = exec_instance.output.decode('utf-8')

            socketio.emit('terminal_output', {'output': output})

        except docker.errors.NotFound:
            socketio.emit('terminal_output', {'output': f"Container {container_id} not found."})
        except Exception as e:
            socketio.emit('terminal_output', {'output': f"Error sending input: {str(e)}"})