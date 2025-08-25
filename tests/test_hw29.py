from conftest import config
import pytest
import requests
import xml.etree.ElementTree as ET

pytestmark = pytest.mark.skipif(not config.get("hw29", False), reason="HW disabled in the config file!")


def test_flask_html_response(flask_container, request):
    url = "http://localhost:8866"
    response = requests.get(url)

    assert response.status_code == 200, "Appication did not run correctly"
    assert "text/html" in response.headers["Content-Type"], "HTML should be returned"

    root = ET.fromstring(response.text)
    img_url = None
    for elem in root.iter():
        if elem.tag == "img":
            img_url = elem.attrib.get("src")
            break

    assert img_url, "There is no HTML tag <img>"
    if not img_url.startswith("https"):
        img_url = f"http://localhost:8866{img_url}"

    request.config.cache.set('URL', img_url)


def test_flask_image_response(request):
    url = request.config.cache.get('URL', None)
    assert url, f"URL should be present in pytest cache, but {url}"

    response = requests.get(url)
    assert response.status_code == 200, "Gif file was not loaded"
    assert "image/gif" in response.headers["Content-Type"], "Response should contain gif file"
