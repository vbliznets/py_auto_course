import json
import time
from docker import from_env
from pytest import fixture


def load_config():
    with open("config/tasks.json", "r", encoding="utf-8") as file:
        return json.load(file)


config = load_config()


@fixture(scope="module")
def flask_container():
    client = from_env()

    container = client.containers.run(
        "flask_cat_app",  # Image name (You must build it, before test execution run!!1!)
        detach=True,
        ports={"5001/tcp": 8866}
    )

    time.sleep(5)

    yield container

    container.stop()
    container.remove()
