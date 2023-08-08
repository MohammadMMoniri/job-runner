import docker

docker_client = docker.from_env()


def search_image(inp):
    return docker_client.images.search(inp)


def build_image():
    pass
